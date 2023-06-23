import sys
import signal
import time
import importlib
import numpy as np
import cv2
import rospy
import traceback
import pymap3d
from collections import deque
from rviz import bindings as rviz
from std_msgs.msg import String, Float32, Int8, Int16MultiArray
from geometry_msgs.msg import PoseStamped, Pose, PoseArray, Point
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
from PyQt5 import uic
import pyqtgraph as pg
import subprocess
import shlex
from selfdrive.message.messaging import *
from sensor_msgs.msg import CompressedImage

import selfdrive.visualize.libs.imugl as imugl
from simple_writer import SimpleWriter
from tl_simulator import TLSimulator
from blinker_simulator import BlinkerSimulator
dir_path = str(os.path.dirname(os.path.realpath(__file__)))
form_class = uic.loadUiType(dir_path+"/forms/main.ui")[0]

MPH_TO_KPH = 3.6

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.car_name = str(self.car_name_combo_box.currentText())
        self.map_name = str(self.map_name_combo_box.currentText())

        self.CP = None
        self.CS = None
        self.CC = None
        self.sm = None
        self.cm = None
        self.imu_widget = None
        self.system_state = False
        self.over_cnt = 0
        self.can_cmd = 0
        self.mode = 0
        self.scenario = 0
        self.goal_update = True
        self.moving_start = False
        self.map_view_manager = None
        self.lidar_view_manager = None
        self.record_list_file = "{}/record_list.txt".format(dir_path)
        self.rosbag_proc = None
        self.media_thread = None
        self.goal_lat, self.goal_lng, self.goal_alt = 0, 0, 0
        
        self.tick = {1: 0, 0.5: 0, 0.2: 0, 0.1: 0, 0.05: 0, 0.02: 0}

        rospy.Subscriber('/move_base_simple/single_goal',PoseStamped, self.goal_cb)
        rospy.Subscriber('/mobinha/planning/target_v',Float32, self.target_v_cb)
        rospy.Subscriber('/mobinha/planning_state',Int16MultiArray, self.planning_state_cb)
        rospy.Subscriber('/mobinha/planning/goal_information',Pose, self.goal_information_cb)
        rospy.Subscriber('/mobinha/perception/nearest_obstacle_distance',Float32, self.nearest_obstacle_distance_cb)
        rospy.Subscriber('/mobinha/perception/traffic_light_obstacle',PoseArray, self.traffic_light_obstacle_cb)
        rospy.Subscriber('/mobinha/planning/trajectory',PoseArray, self.trajectory_cb)
        rospy.Subscriber('/mobinha/planning/lane_information',Pose, self.lane_information_cb)
        rospy.Subscriber('/mobinha/perception/lidar_bsd', Point, self.lidar_bsd_cb)
        rospy.Subscriber('/gmsl_camera/dev/video0/compressed',CompressedImage, self.compressed_image_cb, 1)
        rospy.Subscriber('/gmsl_camera/dev/video1/compressed',CompressedImage, self.compressed_image_cb, 2)
        rospy.Subscriber('/gmsl_camera/dev/video2/compressed',CompressedImage, self.compressed_image_cb, 3)

        self.state = 'WAITING'
        # 0:wait, 1:start, 2:initialize
        self.pub_state = rospy.Publisher('/mobinha/visualize/system_state', String, queue_size=1)
        self.pub_can_cmd = rospy.Publisher('/mobinha/visualize/can_cmd', Int8, queue_size=1)
        self.pub_scenario_goal = rospy.Publisher('/mobinha/visualize/scenario_goal', PoseArray, queue_size=1)

        self.rviz_frame('map')
        self.rviz_frame('lidar')
        self.imu_frame()
        self.information_frame()
        self.graph_frame()
        self.initialize()
        self.connection_setting()

    def timer(self, sec):
        if time.time() - self.tick[sec] > sec:
            self.tick[sec] = time.time()
            return True
        else:
            return False
    
    def setting_topic_list_toggled(self):
        simple_writer = SimpleWriter(self.record_list_file, self)
        simple_writer.show()
        with open(self.record_list_file, 'r') as f:
            contents = f.read()
            simple_writer.textEdit.setText(contents)
    
    def tl_simulator_toggled(self):
        tl_simulator = TLSimulator(self)
        tl_simulator.show()

    def blinker_simulator_toggled(self):
        blinker_simulator = BlinkerSimulator(self)
        blinker_simulator.show()

    def initialize(self):
        rospy.set_param('car_name', self.car_name)
        rospy.set_param('map_name', self.map_name)
        car_class = getattr(sys.modules[__name__], self.car_name)(self.map_name)
        self.CP = car_class.CP
        self.sm = StateMaster(self.CP)
        self.cm = ControlMaster()
        self.pause_button.setDisabled(True)

        if self.radioButton.isChecked():
            path = QFileDialog.getExistingDirectory(None, 'Select folder to save .bag file', QDir.homePath(), QFileDialog.ShowDirsOnly)
            topiclist = ''
            with open(self.record_list_file) as f:
                lines = f.readlines()
                for topic in lines:
                    topiclist += str(topic)+" "
            command = "rosbag record -o {}/ {}".format(str(path), topiclist)
            command = shlex.split(command)
            self.rosbag_proc = subprocess.Popen(command)

    def reset_rviz(self):
        self.lidar_layout.itemAt(0).widget().reset()
        self.rviz_layout.itemAt(0).widget().reset()

    def connection_setting(self):
        self.actionTopic_List.triggered.connect(self.setting_topic_list_toggled)
        self.actionTraffic_Light_Simulator.triggered.connect(self.tl_simulator_toggled)
        self.actionBlinker_Simulator.triggered.connect(self.blinker_simulator_toggled)
        self.initialize_button.clicked.connect(self.initialize_button_clicked)
        self.start_button.clicked.connect(self.start_button_clicked)
        self.pause_button.clicked.connect(self.pause_button_clicked)
        self.over_button.clicked.connect(self.over_button_clicked)
        self.car_name_combo_box.currentIndexChanged.connect(self.car_name_changed)
        self.map_name_combo_box.currentIndexChanged.connect(self.map_name_changed)

        self.can_cmd_buttons = [self.cmd_disable_button, self.cmd_full_button, self.cmd_only_lat_button, self.cmd_only_long_button]
        for i in range(4):
            self.can_cmd_buttons[i].clicked.connect(lambda state, idx=i: self.cmd_button_clicked(idx))

        self.scenario1_button.clicked.connect(lambda state, idx=1:  self.scenario_button_clicked(idx))
        self.scenario2_button.clicked.connect(lambda state, idx=2:  self.scenario_button_clicked(idx))
        self.scenario3_button.clicked.connect(lambda state, idx=3:  self.scenario_button_clicked(idx))

        self.view_third_button.clicked.connect(lambda state, idx=0: self.view_button_clicked(idx))
        self.view_top_button.clicked.connect(lambda state, idx=1: self.view_button_clicked(idx))
        self.view_xy_top_button.clicked.connect(lambda state, idx=2: self.view_button_clicked(idx))

        self.media_thread = MediaThread()
        self.media_thread.start()

    def get_scenario_goal_msg(self):
        scenario_goal = PoseArray() 
        for goal in self.scenario_goal:
            pose = Pose()
            pose.position.x = goal[0]
            pose.position.y = goal[1]
            scenario_goal.poses.append(pose)
        return scenario_goal

    def visualize_update(self):
        while self.system_state:
            if self.timer(0.1):
                self.pub_state.publish(String(self.state))
                self.pub_can_cmd.publish(Int8(self.can_cmd))
                if self.state == 'START':
                    if self.goal_update and self.scenario != 0:
                        scenario_goal = self.get_scenario_goal_msg()
                        self.pub_scenario_goal.publish(scenario_goal)
                        
                    self.sm.update()
                    self.cm.update()
                    self.CS = self.sm.CS
                    self.CC = self.cm.CC
                    self.display()
                elif self.state == 'OVER':
                    self.media_thread.status = False
                    self.over_cnt += 1
                    if(self.over_cnt == 30):
                        self.media_thread.quit()
                        self.media_thread.wait()
                        print("[Visualize] Over")
                        sys.exit(0)
                # elif self.state == 'TOR':

                
                QCoreApplication.processEvents()

    def rviz_frame(self, type):
        rviz_frame = rviz.VisualizationFrame()
        rviz_frame.setSplashPath("")
        rviz_frame.initialize()
        reader = rviz.YamlConfigReader()

        if type == 'map':
            config = rviz.Config()
            reader.readFile(config, dir_path+"/forms/main.rviz")
            rviz_frame.load(config)
            manager = rviz_frame.getManager()
            self.map_view_manager = manager.getViewManager()
            self.clear_layout(self.rviz_layout)
            self.rviz_layout.addWidget(rviz_frame)

        else:
            config = rviz.Config()
            reader.readFile(config, dir_path+"/forms/lidar.rviz")
            rviz_frame.load(config)
            rviz_frame.setMenuBar(None)
            rviz_frame.setStatusBar(None)
            manager = rviz_frame.getManager()
            self.lidar_view_manager = manager.getViewManager()
            self.clear_layout(self.lidar_layout)
            self.lidar_layout.addWidget(rviz_frame)

    def imu_frame(self):
        self.imu_widget = imugl.ImuGL()
        self.imu_layout.addWidget(self.imu_widget)

    def create_graph_widget(self, t, xmin, xmax, ymin, ymax):
        widget = pg.PlotWidget(title=t)
        widget.setBackground('#000A14')
        widget.setXRange(xmin, xmax)
        widget.setYRange(ymin, ymax)
        widget.addLegend()
        return widget

    def graph_frame(self):
        self.graph_timer = QTimer()
        self.graph_time = 0

        self.graph_velocity_data = {'x': deque([0]), 'ye': deque([0]), 'yt': deque([0])}
        self.graph_acceleration_data = {'x': deque([0]), 'ya': deque([0]), 'yb': deque([0])}
        self.graph_steer_data = {'x': deque([0]), 'ye': deque([0]), 'yt': deque([0])}

        self.graph_velocity_widget = self.create_graph_widget("Velocity", 0, 10, 0, 60)
        self.graph_acceleration_widget = self.create_graph_widget("Ego Acceleration",0, 10, -20, 20)
        self.graph_steer_widget = self.create_graph_widget("Steer", 0, 10, -35, 35)

        self.graph_velocity_widget.setLabel('left', 'v', units='km/h')
        self.graph_acceleration_widget.setLabel('left', 'p', units='Ba')
        self.graph_steer_widget.setLabel('left', 'a', units='deg')
        self.graph_layout.addWidget(self.graph_velocity_widget)
        self.graph_layout.addWidget(self.graph_acceleration_widget)
        self.graph_layout.addWidget(self.graph_steer_widget)

        for i in range(self.graph_layout.count()):
            self.graph_layout.itemAt(i).widget().setMaximumSize(300, 200)
            self.graph_layout.itemAt(i).widget().setMinimumSize(300, 200)
            self.graph_layout.itemAt(i).widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        pen_e = pg.mkPen(color='#1363DF', width=3)
        pen_t = pg.mkPen(color='#df1354', width=3)
        pen_a = pg.mkPen(color='#10dea0', width=3)
        pen_b = pg.mkPen(color='#dede10', width=3)
        self.graph_velocity_ego_plot = self.graph_velocity_widget.plot(pen=pen_e, name='Ego')
        self.graph_velocity_target_plot = self.graph_velocity_widget.plot(pen=pen_t, name='Target')
        self.graph_acceleration_accel_plot = self.graph_acceleration_widget.plot(pen=pen_a, name='Accel')
        self.graph_acceleration_brake_plot = self.graph_acceleration_widget.plot(pen=pen_b, name='Brake')
        self.graph_steer_ego_plot = self.graph_steer_widget.plot(pen=pen_e, name='Ego')
        self.graph_steer_target_plot = self.graph_steer_widget.plot(pen=pen_t, name='Target')
        self.graph_velocity_ego_plot.setAlpha(0.7, False)
        self.graph_velocity_target_plot.setAlpha(0.7, False)
        self.graph_acceleration_accel_plot.setAlpha(0.7, False)
        self.graph_acceleration_brake_plot.setAlpha(0.7, False)
        self.graph_steer_ego_plot.setAlpha(0.7, False)
        self.graph_steer_target_plot.setAlpha(0.7, False)

        self.graph_timer.timeout.connect(self.graph_update)
        self.graph_timer.start(500)

    def information_frame(self):
        self.trajectory_widget = pg.PlotWidget()
        self.trajectory_widget.setBackground('#000A14')
        self.trajectory_widget.setXRange(-10, 10)
        self.trajectory_widget.setYRange(0, 10)
        self.trajectory_widget.getPlotItem().hideAxis('bottom')
        self.trajectory_widget.getPlotItem().hideAxis('left')

        self.trajectory_layout.addWidget(self.trajectory_widget)
        pen = pg.mkPen(color='#1363DF', width=120)
        self.trajectory_plot = self.trajectory_widget.plot(pen=pen)

        direction_image_list = [dir_path+"/icon/straight_b.png", dir_path+"/icon/left_b.png", dir_path+"/icon/right_b.png",dir_path+"/icon/uturn_b.png"]
        self.direction_pixmap_list = []
        for i in range(4):
            self.direction_pixmap_list.append(QPixmap(direction_image_list[i]))
        self.direction_message_list = ['Go Straight', 'Turn Left', 'Turn Right', 'U-Turn']

        l_blinker = QPixmap(dir_path+"/icon/l_blinker.png")
        r_blinker = QPixmap(dir_path+"/icon/r_blinker.png")

        self.blinker_l_label.setPixmap(l_blinker)
        self.blinker_r_label.setPixmap(r_blinker)

        self.blinker_l_label.setHidden(True)
        self.blinker_r_label.setHidden(True)

        self.gear_label_list = [self.gear_p_label, self.gear_r_label, self.gear_n_label, self.gear_d_label]

        self.obstacle_pixmap_list = [QPixmap(dir_path+"/icon/object_car_b.png"), QPixmap(dir_path+"/icon/object_pedestrian_b.png")]
        self.distance_pixmap = QPixmap(dir_path+"/icon/distance.png")
        self.distance_label_list = [self.distance_1_label, self.distance_2_label, self.distance_3_label, self.distance_4_label]
        self.tl_label_list = [self.tl_red_label, self.tl_yellow_label, self.tl_arrow_label, self.tl_green_label]

    def clear_layout(self, layout):
        for i in range(layout.count()):
            layout.itemAt(i).widget().close()
            layout.takeAt(i)

    def car_name_changed(self, car_idx):
        self.car_name = str(self.car_name_combo_box.currentText())

    def map_name_changed(self, map_idx):
        self.map_name = str(self.map_name_combo_box.currentText())

    def target_v_cb(self, msg):
        self.label_target_v.setText(f"{round(msg.data*MPH_TO_KPH)} km/h")
        self.target_v = float(round(msg.data*MPH_TO_KPH, 2))

    def graph_update(self):
        if self.moving_start:
            self.graph_time += 0.5
            self.graph_velocity_data['x'].append(self.graph_time)
            self.graph_velocity_data['yt'].append(self.target_v)
            self.graph_velocity_data['ye'].append(self.CS.vEgo*MPH_TO_KPH)
            self.graph_acceleration_data['x'].append(self.graph_time)
            self.graph_acceleration_data['ya'].append(round(self.CS.actuators.accel, 3))
            self.graph_acceleration_data['yb'].append(-round(self.CS.actuators.brake, 3))
            self.graph_steer_data['x'].append(self.graph_time)
            self.graph_steer_data['yt'].append(0)
                #round(self.CC.actuators.steer*self.CP.steerRatio, 3))
            self.graph_steer_data['ye'].append(round(self.CC.cruiseControl.accerror,2))
                #round(self.CS.actuators.steer*self.CP.steerRatio, 3))

            axX_velocity = self.graph_velocity_widget.getAxis('bottom')
            axX_acceleration = self.graph_acceleration_widget.getAxis('bottom')
            axX_steer = self.graph_steer_widget.getAxis('bottom')

            if self.graph_time >= axX_velocity.range[1]:
                self.graph_velocity_widget.setXRange(axX_velocity.range[0]+0.5, axX_velocity.range[1]+0.5, padding=0)
                self.graph_acceleration_widget.setXRange(axX_acceleration.range[0]+0.5, axX_acceleration.range[1]+0.5, padding=0)
                self.graph_steer_widget.setXRange(axX_steer.range[0]+0.5, axX_steer.range[1]+0.5, padding=0)
                self.graph_velocity_data['x'].popleft()
                self.graph_velocity_data['yt'].popleft()
                self.graph_velocity_data['ye'].popleft()
                self.graph_acceleration_data['x'].popleft()
                self.graph_acceleration_data['ya'].popleft()
                self.graph_acceleration_data['yb'].popleft()
                self.graph_steer_data['x'].popleft()
                self.graph_steer_data['yt'].popleft()
                self.graph_steer_data['ye'].popleft()

            if self.state != 'OVER' and self.tabWidget.currentIndex() == 0:
                self.graph_velocity_ego_plot.setData(x=self.graph_velocity_data['x'], y=self.graph_velocity_data['ye'])
                self.graph_velocity_target_plot.setData(x=self.graph_velocity_data['x'], y=self.graph_velocity_data['yt'])
                self.graph_acceleration_accel_plot.setData(x=self.graph_acceleration_data['x'], y=self.graph_acceleration_data['ya'])
                self.graph_acceleration_brake_plot.setData(x=self.graph_acceleration_data['x'], y=self.graph_acceleration_data['yb'])
                self.graph_steer_ego_plot.setData(x=self.graph_steer_data['x'], y=self.graph_steer_data['ye'])
                self.graph_steer_target_plot.setData(x=self.graph_steer_data['x'], y=self.graph_steer_data['yt'])

    def goal_cb(self, msg):
        self.goal_x_label.setText(str(round(msg.pose.position.x, 5)))
        self.goal_y_label.setText(str(round(msg.pose.position.y, 5)))

        self.goal_lat, self.goal_lng, self.goal_alt = pymap3d.enu2geodetic(msg.pose.position.x, msg.pose.position.y, 0,self.CP.mapParam.baseLatitude, self.CP.mapParam.baseLongitude, self.CP.mapParam.baseAltitude)

    def goal_information_cb(self, msg):
        m_distance = msg.position.y-msg.position.z
        distance = f"{(m_distance/1000.0):.5f} km" if m_distance / 1000 >= 1 else f"{m_distance:.5f} m"
        self.goal_distance_label.setText(distance)

    def nearest_obstacle_distance_cb(self, msg):
        self.label_obstacle_distance.setText(str(round(msg.data, 5))+" m")  # nearest obstacle

        if self.state != 'OVER' and self.tabWidget.currentIndex() == 4:
            if msg.data > 0 and msg.data <= 7:
                for i in range(1, 4):
                    self.distance_label_list[i].setText("")
                self.distance_label_list[0].setText("❗️")
            elif msg.data > 7 and msg.data <= 15:
                for i in range(2, 4):
                    self.distance_label_list[i].setText("")
                self.distance_label_list[1].setText("❗️")
                self.distance_label_list[0].setText("7m")
            elif msg.data > 15 and msg.data <= 30:
                self.distance_label_list[3].setText("")
                self.distance_label_list[2].setText("❗️")
                self.distance_label_list[1].setText("15m")
                self.distance_label_list[0].setText("7m")
            elif msg.data > 30:
                self.distance_label_list[3].setText("❗️")
                self.distance_label_list[2].setText("30m")
                self.distance_label_list[1].setText("15m")
                self.distance_label_list[0].setText("7m")
            elif msg.data < 0:
                self.distance_label_list[3].setText("")
                self.distance_label_list[2].setText("30m")
                self.distance_label_list[1].setText("15m")
                self.distance_label_list[0].setText("7m")

    def traffic_light_obstacle_cb(self, msg):
        tl_on_list = ["🔴", "🟡", "⬅️", "🟢"]
        tl_off = "⬛️"

        if len(msg.poses) == 0:
            for i in range(4):
                self.tl_label_list[i].setText(tl_off)
            return 
        if self.state == 'OVER' or self.tabWidget.currentIndex() != 4:
            return
        
        tl_cls = msg.poses[0].position.y
        tl_cls_list = [[6, 10, 12, 13, 15], [8, 11, 13, 16], [12, 14], [4, 9, 14, 17]]
        tl_detect_cls = [i for i, cls in enumerate(tl_cls_list) if tl_cls in cls]
        for i in range(4):
            self.tl_label_list[i].setText(tl_on_list[i] if i in tl_detect_cls else tl_off)


    def trajectory_cb(self, msg):
        if self.state != 'OVER' and self.tabWidget.currentIndex() == 4:
            x = [v.position.x for v in msg.poses]
            y = [v.position.y for v in msg.poses]

            self.trajectory_plot.clear()
            self.trajectory_plot.setData(x=x, y=y)
            self.info_curvature_label.setText(f"{msg.poses[0].position.z:.1f} m")
    
    def lidar_bsd_cb(self, msg):
        if self.state != 'OVER' and self.tabWidget.currentIndex() == 4:
            if msg.x == 1:
                self.bsd_l_label.setText("❗️")
            else:
                self.bsd_l_label.setText(" ")
            if msg.y == 1:
                self.bsd_r_label.setText("❗️")
            else:
                self.bsd_r_label.setText(" ")
                
        elif self.state != 'OVER':
            if msg.x == 1 and self.CS.buttonEvent.leftBlinker == 1:
                self.media_thread.get_mode = 3
            if msg.y == 1 and self.CS.buttonEvent.rightBlinker == 1:
                self.media_thread.get_mode = 4

    def lane_information_cb(self, msg):
        if self.state != 'OVER' and self.tabWidget.currentIndex() == 4:
            idx = int(msg.position.y)
            self.direction_text_label.setText(self.direction_message_list[idx])
            self.direction_image_label.setPixmap(self.direction_pixmap_list[idx])

    def convert_to_qimage(self, data):
        np_arr = np.frombuffer(data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        rgbImage = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bpl = ch * w
        qtImage = QImage(rgbImage.data, w, h, bpl, QImage.Format_RGB888)
        return qtImage.scaled(self.camera1_label.width(), self.camera1_label.height(), Qt.KeepAspectRatio)

    def compressed_image_cb(self, data,arg):
        if self.state != 'OVER' and self.tabWidget.currentIndex() == 2:
            qImage = self.convert_to_qimage(data.data)
            label_list = [self.camera1_label, self.camera2_label, self.camera3_label]
            label_list[arg-1].setPixmap(QPixmap.fromImage(qImage))

    def planning_state_cb(self, msg):
        if msg.data[0] == 1 and msg.data[1] == 1:
            # self.state = 'START'
            self.status_label.setText("Moving")
            self.moving_start = True
            self.goal_update = False
            self.scenario1_button.setDisabled(True)
            self.scenario2_button.setDisabled(True)
            self.scenario3_button.setDisabled(True)

        elif msg.data[0] == 2 and msg.data[1] == 2:
            self.status_label.setText("Arrived")
            self.cmd_button_clicked(0)
            self.pause_button.setDisabled(True)
            self.start_button.setEnabled(True)
            self.initialize_button.setEnabled(True)

        elif msg.data[0] == 3:
            self.status_label.setText("Insert Goal")
            self.scenario1_button.setEnabled(True)
            self.scenario2_button.setEnabled(True)
            self.scenario3_button.setEnabled(True)

        elif msg.data[0] == 4:
            # self.state = 'TOR'
            self.status_label.setText("Take Over Request")
            self.cmd_button_clicked(0)
            # self.start_button.setDisabled(True)
            # self.initialize_button.setEnabled(True)
            # self.pause_button.setDisabled(True)
            self.start_button.setDisabled(True)
            self.initialize_button.setDisabled(True)
            self.pause_button.setEnabled(True)

    def start_button_clicked(self):
        self.state = 'START'
        self.status_label.setText("Starting ...")
        self.start_button.setDisabled(True)
        self.initialize_button.setDisabled(True)
        self.pause_button.setEnabled(True)

    def pause_button_clicked(self):
        self.state = 'PAUSE'
        self.status_label.setText("Pause")
        self.start_button.setEnabled(True)
        self.initialize_button.setEnabled(True)
        self.pause_button.setDisabled(True)

    def initialize_button_clicked(self):
        self.status_label.setText("Initialize")
        self.initialize()
        self.goal_update = True
        # self.reset_rviz()
        self.start_button.setEnabled(True)
        self.scenario = 0
        self.scenario1_button.setDisabled(True)
        self.scenario2_button.setDisabled(True)
        self.scenario3_button.setDisabled(True)
        self.state = 'INITIALIZE'

    def over_button_clicked(self):
        self.status_label.setText("Over")
        self.graph_timer.stop()
        rospy.set_param('car_name', 'None')
        rospy.set_param('map_name', 'None')
        if self.rosbag_proc is not None:
            self.rosbag_proc.send_signal(subprocess.signal.SIGINT)
        self.state = 'OVER'

    def cmd_button_clicked(self, idx):
        self.can_cmd = idx
        for i in range(1, 4):
            self.can_cmd_buttons[i].setDisabled(i != idx)
        if idx == 0:
            for button in self.can_cmd_buttons:
                button.setEnabled(True)

    def scenario_button_clicked(self, idx):
        self.scenario = idx
        module = importlib.import_module('selfdrive.visualize.routes.{}'.format(self.map_name))
        scenario = getattr(module, 'scenario_{}'.format(idx))
        self.scenario_goal = scenario

    def view_button_clicked(self, idx):
        if self.map_view_manager is not None:
            self.map_view_manager.setCurrentFrom(self.map_view_manager.getViewAt(idx))

    def get_mode_label(self, mode):
        if mode == 1:
            return "Auto"
        elif mode == 2:
            return "Override"
        else:
            return "Manual"


    def check_mode(self, mode):
        if self.mode != mode:
            self.mode = mode
            if self.media_thread != None:
                self.media_thread.get_mode = mode
            if mode == 2:
                self.cmd_button_clicked(0) #act like click disable button


    def display(self):
        self.label_vehicle_vel.setText(f"{round(self.CS.vEgo*MPH_TO_KPH)} km/h")
        self.label_vehicle_yaw.setText(f"{self.CS.yawRate:.5f} deg")
        self.label_target_yaw.setText(f"{(float(self.CC.actuators.steer*self.CP.steerRatio)+self.CS.yawRate):.5f} deg")
        self.main_mode_label.setText(f"{self.get_mode_label(self.CS.cruiseState)} Mode")
        self.check_mode(self.CS.cruiseState)

        if self.state != 'OVER' and self.tabWidget.currentIndex() == 3:

            self.imu_widget.updateRP(self.CS.rollRate, self.CS.pitchRate, self.CS.yawRate)
            self.gps_latitude_label.setText(str(self.CS.position.latitude))
            self.gps_longitude_label.setText(str(self.CS.position.longitude))
            self.gps_altitude_label.setText(str(self.CS.position.altitude))
            self.gps_x_label.setText(str(self.CS.position.x))
            self.gps_y_label.setText(str(self.CS.position.y))
            self.gps_z_label.setText(str(self.CS.position.z))
            self.imu_angle_label.setText(f"Y: {self.CS.yawRate}")
            self.imu_angle_label_2.setText(f"P: {self.CS.pitchRate}")
            self.imu_angle_label_3.setText(f"R: {self.CS.rollRate}")
            self.car_velocity_label.setText(f"{round(self.CS.vEgo*MPH_TO_KPH)} km/h")

            self.target_mode_label.setText(self.get_mode_label(self.can_cmd))
            self.car_mode_label.setText(self.get_mode_label(self.CS.cruiseState))
            self.car_steer_angle_label.setText(str(self.CS.actuators.steer))
            self.car_accel_label.setText(str(self.CS.actuators.accel))
            self.car_brake_label.setText(str(self.CS.actuators.brake))

            self.target_steer_angle_label.setText(str(self.CC.actuators.steer))
            self.target_accel_label.setText(str(self.CC.actuators.accel))
            self.target_brake_label.setText(str(self.CC.actuators.brake))

        if self.state != 'OVER' and self.tabWidget.currentIndex() == 4:
            self.info_mode_label.setText(f"{self.get_mode_label(self.CS.cruiseState)} Mode")
            self.info_velocity_label.setText(str(round(self.CS.vEgo*MPH_TO_KPH)))
            self.info_car_lat_label.setText(f"lat : {self.CS.position.latitude:.4f}")
            self.info_car_lng_label.setText(f"lng : {self.CS.position.longitude:.4f}")
            self.info_car_alt_label.setText(f"alt : {self.CS.position.altitude:.4f}")
            self.info_y_label.setText(f"Y: {self.CS.yawRate:.5f}")
            self.info_p_label.setText(f"P: {self.CS.pitchRate:.5f}")
            self.info_r_label.setText(f"R: {self.CS.rollRate:.5f}")

            self.info_goal_lat_label.setText(f"lat : {self.goal_lat:.5f}")
            self.info_goal_lng_label.setText(f"lng : {self.goal_lng:.5f}")
            self.info_goal_alt_label.setText(f"alt : {self.goal_alt:.5f}")

            [self.gear_label_list[i].setStyleSheet("QLabel{color:rgb(19, 99, 223);}") if self.CS.gearShifter == i else self.gear_label_list[i].setStyleSheet("QLabel{color: rgb(223, 246, 255);}") for i in range(4)]

            if self.CS.buttonEvent.leftBlinker == 1:
                self.blinker_l_label.setHidden(False)
                self.blinker_r_label.setHidden(True)
            elif self.CS.buttonEvent.rightBlinker == 1:
                self.blinker_l_label.setHidden(True)
                self.blinker_r_label.setHidden(False)
            elif self.CS.buttonEvent.leftBlinker == 1 and self.CS.buttonEvent.rightBlinker == 1:
                self.blinker_l_label.setHidden(False)
                self.blinker_r_label.setHidden(False)
            else:
                self.blinker_l_label.setHidden(True)
                self.blinker_r_label.setHidden(True)


def signal_handler(sig, frame):
    QApplication.quit()
    sys.exit(0)


class MediaThread(QThread):
    def __init__(self):
        super().__init__()
        self.status = True
        self.mode = 0
        self.get_mode = 0
    
    def run(self):
        player = QMediaPlayer()
        while self.status:
            if self.mode != self.get_mode:
                if self.get_mode == 1:
                    url = dir_path+"/sounds/on.wav"
                    self.mode = self.get_mode
                elif self.get_mode == 3 or self.get_mode == 4:
                    url = dir_path+"/sounds/bsd.wav"
                    self.get_mode = self.mode
                else:
                    url = dir_path+"/sounds/off.wav"
                    self.mode = self.get_mode
                media = QMediaContent(QUrl.fromLocalFile(url))
                player.setMedia(media)
                player.play()
                
            time.sleep(1)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("[Visualize] Created")
    rospy.init_node('Visualize', anonymous=False)

    app = QApplication(sys.argv)

    try:
        mainWindow = MainWindow()
        mainWindow.showNormal()
        mainWindow.system_state = True
        mainWindow.visualize_update()
        if app.exec_() == 0:
            mainWindow.system_state == False
        sys.exit(app.exec_())

    except Exception:
        print("[Visualize Error]", traceback.print_exc())

    except KeyboardInterrupt:
        print("[Visualize] Force Quit")
        mainWindow.close()
        app.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()

