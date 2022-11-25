import sys
import signal
import time

import rospy
from rviz import bindings as rviz
from std_msgs.msg import String, Float32, Int16, Int16MultiArray
from geometry_msgs.msg import PoseStamped, PoseArray
from jsk_recognition_msgs.msg import BoundingBoxArray

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from selfdrive.message.messaging import *

dir_path = str(os.path.dirname(os.path.realpath(__file__)))
form_class = uic.loadUiType(dir_path+"/forms/main.ui")[0]

MPH_TO_KPH = 3.6


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.car_name = str(self.car_name_combo_box.currentText())
        self.CP = None
        self.CS = None

        self.finish_cnt = 0
        self.can_cmd = 0
        self.scenario = 0
        self.scenario_goal = PoseStamped()
        self.scenario_goal.header.frame_id = 'world'

        self.sub_wheel_angle = rospy.Subscriber(
            '/wheel_angle', Float32, self.wheel_angle_cb)
        self.sub_target_v = rospy.Subscriber(
            '/target_v', Float32, self.target_v_cb)
        self.sub_planning_state = rospy.Subscriber(
            '/planning_state', Int16MultiArray, self.planning_state_cb)
        self.sub_goal = rospy.Subscriber(
            '/move_base_simple/goal', PoseStamped, self.goal_cb)
        self.sub_distance_to_goal = rospy.Subscriber(
            '/distance_to_goal', Float32, self.distance_to_goal_cb)
        self.sub_nearest_obstacle_distance = rospy.Subscriber(
            '/nearest_obstacle_distance', Float32, self.nearest_obstacle_distance_cb)

        self.state: str = 'WAITING'
        # 0:wait, 1:start, 2:initialize
        self.pub_state = rospy.Publisher('/state', String, queue_size=1)
        self.pub_can_cmd = rospy.Publisher('/can_cmd', Int16, queue_size=1)

        self.pub_goal = rospy.Publisher(
            '/move_base_simple/goal', PoseStamped, queue_size=1)

        self.initialize()
        self.connection_setting()

    def initialize(self):
        car_class = getattr(sys.modules[__name__], self.car_name)
        rospy.set_param('car_name', self.car_name)
        self.CP = car_class.CP

        # setting rviz
        self.rviz_frame = rviz.VisualizationFrame()
        self.rviz_frame.setSplashPath("")
        self.rviz_frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile(config, dir_path+"/forms/main.rviz")
        self.rviz_frame.load(config)
        self.manager = self.rviz_frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt(0)
        self.rviz_layout.addWidget(self.rviz_frame)

        # setting button
        self.pause_button.setDisabled(True)
        self.initialize_button.setDisabled(True)

    def connection_setting(self):
        self.start_button.clicked.connect(self.start_button_clicked)
        self.pause_button.clicked.connect(self.pause_button_clicked)
        self.initialize_button.clicked.connect(self.initialize_button_clicked)
        self.finish_button.clicked.connect(self.finish_button_clicked)
        self.car_name_combo_box.currentIndexChanged.connect(
            self.car_name_changed)
        self.cmd_full_button.clicked.connect(self.cmd_full_button_clicked)
        self.cmd_disable_button.clicked.connect(
            self.cmd_disable_button_clicked)
        self.cmd_only_lat_button.clicked.connect(
            self.cmd_only_lat_button_clicked)
        self.cmd_only_long_button.clicked.connect(
            self.cmd_only_long_button_clicked)

        self.scenario1_button.clicked.connect(self.scenario1_button_clicked)
        self.scenario2_button.clicked.connect(self.scenario2_button_clicked)
        self.scenario3_button.clicked.connect(self.scenario3_button_clicked)

    def car_name_changed(self, car_name):
        self.initialize()

    def wheel_angle_cb(self, msg):
        self.label_target_yaw.setText(
            str(round(float(msg.data*self.CP.steerRatio)+self.CS.yawRate, 5))+" deg")

    def target_v_cb(self, msg):
        self.label_target_v.setText(
            str(float(round(msg.data*MPH_TO_KPH)))+" km/h")

    def goal_cb(self, msg):
        self.goal_x_label.setText(str(round(msg.pose.position.x, 5)))
        self.goal_y_label.setText(str(round(msg.pose.position.y, 5)))

    def distance_to_goal_cb(self, msg):
        distance = str(round(msg.data / 1000, 5))+" km" if msg.data / \
            1000 >= 1 else str(round(msg.data, 5))+" m"
        self.goal_distance_label.setText(distance)

    def nearest_obstacle_distance_cb(self, msg):
        self.label_obstacle_distance.setText(
            str(round(msg.data, 5))+" m")  # nearest obstacle

    def planning_state_cb(self, msg):
        if msg.data[0] == 1 and msg.data[1] == 1:
            self.status_label.setText("Moving")
            self.start_button.setDisabled(True)
            self.initialize_button.setDisabled(True)
            self.pause_button.setEnabled(True)
            self.scenario1_button.setDisabled(True)
            self.scenario2_button.setDisabled(True)
            self.scenario3_button.setDisabled(True)

        elif msg.data[0] == 2 and msg.data[1] == 2:
            self.status_label.setText("Arrived")
            self.pause_button.setDisabled(True)
            self.start_button.setEnabled(True)
            self.initialize_button.setEnabled(True)

        elif msg.data[0] == 3:
            self.status_label.setText("Insert Goal")
            self.scenario1_button.setEnabled(True)
            self.scenario2_button.setEnabled(True)
            self.scenario3_button.setEnabled(True)

        elif msg.data[0] == 4:
            self.state == 'TOR'
            self.status_label.setText("Take Over Request")
            self.start_button.setDisabled(True)
            self.initialize_button.setEnabled(True)
            self.pause_button.setDisabled(True)

    def start_button_clicked(self):
        sm = StateMaster(CP)
        self.state = 'START'
        while True:
            self.pub_state.publish(String(self.state))
            self.pub_can_cmd.publish(Int16(self.can_cmd))
            if self.state == 'START':
                if self.scenario != 0:
                    self.pub_goal.publish(self.scenario_goal)
                sm.update()
                self.CS = sm.CS
                self.display()
            elif self.state == 'PAUSE':
                self.status_label.setText("Pause")
                self.start_button.setEnabled(True)
                self.initialize_button.setEnabled(True)
                self.pause_button.setDisabled(True)
            elif self.state == 'INITIALIZE':
                self.status_label.setText("Stand by")
                self.start_button.setEnabled(True)
                self.scenario = 0
            elif self.state == 'FINISH':
                self.status_label.setText("Over")
                self.finish_cnt += 1
                if(self.finish_cnt == 20):
                    print("[Visualize] Over")
                    sys.exit(0)
            time.sleep(0.1)
            QApplication.processEvents()

    def pause_button_clicked(self):
        self.state = 'PAUSE'

    def initialize_button_clicked(self):
        self.state = 'INITIALIZE'

    def finish_button_clicked(self):
        self.state = 'FINISH'

    def cmd_disable_button_clicked(self):
        self.can_cmd = 0

    def cmd_full_button_clicked(self):
        self.can_cmd = 2 if self.can_cmd == 3 else 3

    def cmd_only_lat_button_clicked(self):
        self.can_cmd = 2 if self.can_cmd == 1 else 1

    def cmd_only_long_button_clicked(self):
        self.can_cmd = 2 if self.can_cmd == 4 else 4

    def scenario1_button_clicked(self):
        self.scenario = 1
        self.scenario_goal.pose.position.x = 110.51365
        self.scenario_goal.pose.position.y = -219.24281

    def scenario2_button_clicked(self):
        self.scenario = 2
        self.scenario_goal.pose.position.x = 105.68604
        self.scenario_goal.pose.position.y = -92.7337

    def scenario3_button_clicked(self):
        self.scenario = 3
        self.scenario_goal.pose.position.x = 394.54889
        self.scenario_goal.pose.position.y = -12.554

    def display(self):
        self.label_vehicle_vel.setText(
            str(float(round(self.CS.vEgo*MPH_TO_KPH)))+" km/h")
        self.label_vehicle_yaw.setText(str(round(self.CS.yawRate, 5))+" deg")


def signal_handler(sig, frame):
    QApplication.quit()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("[Visualize] Created")
    rospy.init_node('Visualize', anonymous=False)

    app = QApplication(sys.argv)

    try:
        mainWindow = MainWindow()
        mainWindow.showMinimized()
        sys.exit(app.exec_())

    except Exception as e:
        print("[Visualize Error]", e)

    except KeyboardInterrupt:
        print("[Visualize] Force Quit")
        mainWindow.close()
        app.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
