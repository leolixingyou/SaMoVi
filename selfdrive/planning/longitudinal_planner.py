import rospy
import math

from std_msgs.msg import Float32
from geometry_msgs.msg import PoseArray, Pose

from selfdrive.planning.libs.planner_utils import *
from selfdrive.visualize.rviz_utils import *

from collections import deque

import csv
import datetime
import os

KPH_TO_MPS = 1 / 3.6
MPS_TO_KPH = 3.6
HZ = 10

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f'acc_test_data_{current_time}.csv'

def write_to_csv(data):
    # file_name = 'variables.csv'

    is_new_file = not os.path.exists(file_name)

    with open(file_name, mode='a') as csvfile:
        writer = csv.writer(csvfile)
        if is_new_file:
            header = ['timestamp', 'near_obj_id', 'v_lead(km/h)', 
                      'desired_follow_d(m)', 'front_car_d(-10)(m)', 'error', 'acc(m/s^2)']
            writer.writerow(header)

        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data.insert(0, current_timestamp)
        writer.writerow(data)

class LongitudinalPlanner:
    def __init__(self, CP):

        self.lidar_obstacle = None
        self.traffic_light_obstacle = None
        self.lane_information = None
        self.goal_object = None
        self.M_TO_IDX = 1/CP.mapParam.precision
        self.IDX_TO_M = CP.mapParam.precision

        self.ref_v = CP.maxEnableSpeed
        self.min_v = CP.minEnableSpeed
        self.target_v = 0  # self.min_v*KPH_TO_MPS
        self.st_param = CP.stParam._asdict()
        self.sl_param = CP.slParam._asdict()

        self.last_error = 0
        self.last_s = None
        self.follow_error = 0
        self.integral = 0
        self.rel_v = 0
        self.distance_queue = deque(maxlen=5)

        rospy.Subscriber(
            '/mobinha/perception/lidar_obstacle', PoseArray, self.lidar_obstacle_cb)
        rospy.Subscriber('/mobinha/perception/traffic_light_obstacle',
                         PoseArray, self.traffic_light_obstacle_cb)
        rospy.Subscriber('/mobinha/planning/lane_information',
                         Pose, self.lane_information_cb)
        rospy.Subscriber(
            '/mobinha/planning/goal_information', Pose, self.goal_object_cb)
        self.pub_target_v = rospy.Publisher(
            '/mobinha/planning/target_v', Float32, queue_size=1, latch=True)
        self.pub_traffic_light_marker = rospy.Publisher(
            '/mobinha/planner/traffic_light_marker', Marker, queue_size=1)
        self.pub_accerror = rospy.Publisher('/mobinha/control/accerror', Float32, queue_size=1)

    def lidar_obstacle_cb(self, msg):
        self.lidar_obstacle = [(pose.position.x, pose.position.y, pose.position.z, pose.orientation.w)
                               for pose in msg.poses]

    def traffic_light_obstacle_cb(self, msg):
        self.traffic_light_obstacle = [(pose.position.x, pose.position.y, pose.position.z)
                                       for pose in msg.poses]

    def lane_information_cb(self, msg):
        # [0] id, [1] forward_direction, [2] cross_walk distance [3] forward_curvature
        self.lane_information = [msg.position.x,
                                 msg.position.y, msg.position.z, msg.orientation.x]

    def goal_object_cb(self, msg):
        self.goal_object = (msg.position.x, msg.position.y, msg.position.z)

    def obstacle_handler(self, obj, s):
        # [0] Dynamic [1] Static [2] Traffic Light
        i = int(obj[0])
        offset = [10, 5, 9]  # m
        offset = [os*self.M_TO_IDX for os in offset]
        pos = obj[1] + s if obj[0] == 1 else obj[1]
        return i, pos-offset[i]

    def sigmoid_logit_function(self, s):
        return ((1+((s*(1-self.sl_param["mu"]))/(self.sl_param["mu"]*(1-s)))**-self.sl_param["v"])**-1)

    def get_stoped_equivalence_factor(self, v_lead, comfort_decel=2.5):
        v_lead = max(0, v_lead) # Sumption : back moving car is zero 
        return ((v_lead**2) / (2*comfort_decel))

    def get_safe_obs_distance(self, v_ego, desired_ttc=3, comfort_decel=2.5, offset=3): # cur v = v ego (m/s), 2 sec, 2.5 decel (m/s^2)
        return ((v_ego ** 2) / (2 * comfort_decel) + desired_ttc * v_ego + offset)
    
    def desired_follow_distance(self, v_ego, v_lead=0):
        return max(0, self.get_safe_obs_distance(v_ego) - self.get_stoped_equivalence_factor(v_lead))

    def get_dynamic_gain(self, error, kp=0.15/HZ, ki=0.01/HZ, kd=0.03/HZ):
        self.integral += error*(1/HZ)
        if self.integral > 6:
            self.integral = 6
        elif self.integral < -6:
            self.integral = -6
        derivative = (error - self.last_error)/(1/HZ) #  frame calculate.
        self.last_error = error
        if error < 0:
            return max(0/HZ, min(2.5/HZ, -(kp*error + ki*self.integral + kd*derivative)))
        else:
            return min(0/HZ, max(-7/HZ, -(kp*error + ki*self.integral + kd*derivative)))
    def get_static_gain(self, error, gain=0.4/HZ):
        if error < 0:
            return 2.5 / HZ
        else:
            return max(2.5/HZ, min(7/HZ, error*gain))
    def dynamic_consider_range(self, max_v, base_range=100):  # input max_v unit (m/s)
        return base_range + (0.267*(max_v)**1.902)
    
    def planning_tracking(self, s, cur_v):
        if self.last_s == None:
            self.last_s = s
            return -cur_v
        else:
            ds = s - self.last_s
            self.distance_queue.append(ds)
            if len(self.distance_queue) == 5: # 큐에 5개 이상의 거리 차이가 쌓였을 때
                self.rel_v = sum(self.distance_queue) / len(self.distance_queue) * HZ # 거리 차이의 평균을 이용하여 속도 계산
                self.distance_queue.popleft()
            else:
                self.last_s = s
                return -cur_v
            self.last_s = s
            return self.rel_v
    
    def simple_velocity_plan(self, cur_v, max_v,  local_s, object_list):
        pi = 1
        min_obs_s = 1
        near_obj_id = -1
        consider_distance = self.dynamic_consider_range(self.ref_v*KPH_TO_MPS)
        min_s = 150 # prev 80
        self.rel_v = cur_v
        norm_s = 1
        obj_i = -1
        for obj in object_list:
            obj_i, s = self.obstacle_handler(obj, local_s)  # Remain Distance
            s -= local_s
            if 0 < s < consider_distance:
                norm_s = s/consider_distance
            elif s <= 0:
                norm_s = 0

            if min_obs_s > norm_s:
                min_obs_s = norm_s
                min_s = s*self.IDX_TO_M
                near_obj_id = obj_i
            if len(obj) == 4:
                # planning tracking mode
                # self.rel_v = self.planning_tracking(min_s, cur_v)
                # lidar clustering tracking mode
                self.rel_v = obj[3]

        if 0 < min_obs_s < 1:
            pi = self.sigmoid_logit_function(min_obs_s)
            # if (cur_v-0) == 0 else (follow_error) / (cur_v-0)# TODO : cur_v -> cur_v - obs_v
        elif min_obs_s <= 0:
            pi = 0

        if near_obj_id == 0:
            follow_distance = self.desired_follow_distance(cur_v)#, self.rel_v + cur_v)
        else:
            follow_distance = self.desired_follow_distance(cur_v)
            self.last_s = None # Reset when the car in front is gone.

        self.follow_error = (follow_distance-min_s)
        target_v = max_v * pi
        gain = 2.5/HZ
        # print(near_obj_id,"lead v:", round((self.rel_v + cur_v)*MPS_TO_KPH,1) ,"flw d:", round(follow_distance), "obs d:", round(min_s), "err(0):",round(self.follow_error,2), "gain:",round(gain,3))
        
        if near_obj_id != 0:
            # gain = 2.5/HZ
            gain = self.get_static_gain(self.follow_error)
            data_to_save = [
            near_obj_id,
            0,
            round(follow_distance,1),
            round(min_s,1),
            round(self.follow_error,3),
            round(gain*10,2)
            ]
            write_to_csv(data_to_save)
            if self.target_v-target_v < -gain:
                target_v = self.target_v + gain
            elif self.target_v-target_v > gain:
                target_v = self.target_v - gain
        else:
            gain = self.get_dynamic_gain(self.follow_error)
            # print(near_obj_id,"lead v:", round((self.rel_v + cur_v)*MPS_TO_KPH,1) ,"flw d:", round(follow_distance), "obs d:", round(min_s), "err(0):",round(self.follow_error,2), "gain:",round(gain,3))
            data_to_save = [
            near_obj_id,
            round((self.rel_v + cur_v) * MPS_TO_KPH, 1),
            round(follow_distance,1),
            round(min_s,1),
            round(self.follow_error,3),
            round(gain*10,2)
            ]
            write_to_csv(data_to_save)
            if self.follow_error < 0: # MINUS is ACCEL
                target_v = min(self.ref_v*KPH_TO_MPS, self.target_v + gain)
            else: # PLUS is DECEL
                target_v = max(0, self.target_v + gain)

        return target_v

    def traffic_light_to_obstacle(self, traffic_light, forward_direction):
        # TODO: consideration filtering
        consideration_class_list = [[6, 8, 10, 11, 12, 13], [4, 6, 8, 9, 10, 11, 13], [
            6, 8, 10, 11, 12, 13], [6, 8, 10, 11, 12, 13], [6, 8, 10, 11, 12, 13], [4, 6, 8, 9, 10, 11, 13]]
        if traffic_light in consideration_class_list[forward_direction]:
            return False
        else:
            return True

    def check_objects(self, local_path):
        object_list = []
        local_len = len(local_path)
        # [0] = Dynamic Object
        if self.lidar_obstacle is not None:
            for lobs in self.lidar_obstacle:
                if lobs[2] >= -1.5 and lobs[2] <= 1.5:  # object in my lane
                    object_list.append(lobs) # lobs[3] relative velocity

        # [1] = Goal Object
        if self.goal_object is not None:
            left = (self.goal_object[1]-self.goal_object[2]) * self.M_TO_IDX
            if left <= local_len:
                object_list.append([1, left, 0])

        # [2] = Traffic Light
        if self.traffic_light_obstacle is not None:
            can_go = False
            if len(self.traffic_light_obstacle) > 0:
                tlobs = self.traffic_light_obstacle[0]
                if self.traffic_light_to_obstacle(int(tlobs[1]), int(self.lane_information[1])):
                    can_go = True
            if not can_go:
                if self.lane_information[2] <= math.inf:
                    object_list.append((2, self.lane_information[2], 0))
        return object_list

    def run(self, sm, pp=0, local_path=None):
        CS = sm.CS
        lgp = 0
        self.pub_target_v.publish(Float32(self.target_v))
        self.pub_accerror.publish(Float32(self.follow_error))
        if local_path != None and self.lane_information != None and CS.cruiseState == 1:
            local_idx = calc_idx(
                local_path, (CS.position.x, CS.position.y))
            local_curv_v = max_v_by_curvature(
                self.lane_information[3], self.ref_v, self.min_v)
            object_list = self.check_objects(local_path)

            self.target_v = self.simple_velocity_plan(
                CS.vEgo,  local_curv_v, local_idx, object_list)

            if pp == 2:
                self.target_v = 0.0
                if CS.vEgo <= 0.001:
                    lgp = 2
            elif pp == 4:
                self.target_v = 0.0
            else:
                lgp = 1

        return lgp
