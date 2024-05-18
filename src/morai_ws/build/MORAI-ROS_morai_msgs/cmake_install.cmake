# Install script for directory: /workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspace/mobinha_license/src/morai_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs/msg" TYPE FILE FILES
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/CtrlCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/EgoVehicleStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/EgoVehicleStatusExtended.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/GPSMessage.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/GhostMessage.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ObjectStatusList.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ObjectStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ObjectStatusExtended.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ObjectStatusListExtended.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/TrafficLight.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ERP42Info.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/GetTrafficLightStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SetTrafficLight.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/IntersectionControl.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/IntersectionStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/CollisionData.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MultiEgoSetting.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/IntscnTL.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SensorPosControl.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MoraiSimProcHandle.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MoraiSimProcStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MoraiSrvResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ScenarioLoad.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MoraiTLIndex.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MoraiTLInfo.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SaveSensorData.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/ReplayInfo.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/EventInfo.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/Lamps.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/VehicleSpec.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/VehicleSpecIndex.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/NpcGhostCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/NpcGhostInfo.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/VehicleCollisionData.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/VehicleCollision.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeAddObject.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeInfo.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/WaitForTickResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeRemoveObject.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeCmdResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/WaitForTick.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MapSpec.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MapSpecIndex.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeCtrlCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeSetGear.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeResultResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SyncModeScenarioLoad.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/RadarDetection.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/RadarDetections.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/PRStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/PRCtrlCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/PREvent.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SkateboardCtrlCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SkateboardStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SkidSteer6wUGVCtrlCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SkidSteer6wUGVStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MultiPlayEventResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/MultiPlayEventRequest.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/DillyCmdResponse.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/DillyCmd.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/WoowaDillyStatus.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/SVADC.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultInjection_Controller.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultInjection_Response.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultInjection_Sensor.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultInjection_Tire.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultStatusInfo_Overall.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultStatusInfo_Sensor.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultStatusInfo_Vehicle.msg"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/msg/FaultStatusInfo.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs/srv" TYPE FILE FILES
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiScenarioLoadSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSimProcSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiTLInfoSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiEventCmdSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiVehicleSpecSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeCmdSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiWaitForTickSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiMapSpecSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeCtrlCmdSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeSetGearSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeSLSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/PREventSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeAddObjectSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MoraiSyncModeRemoveObjectSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/MultiPlayEventSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/WoowaDillyEventCmdSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/FaultInjectionCtrlSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/FaultInjectionSensorSrv.srv"
    "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/srv/FaultInjectionTireSrv.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs/cmake" TYPE FILE FILES "/workspace/mobinha_license/src/morai_ws/build/MORAI-ROS_morai_msgs/catkin_generated/installspace/morai_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/workspace/mobinha_license/src/morai_ws/devel/include/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/workspace/mobinha_license/src/morai_ws/devel/share/roseus/ros/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/workspace/mobinha_license/src/morai_ws/devel/share/common-lisp/ros/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/workspace/mobinha_license/src/morai_ws/devel/share/gennodejs/ros/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/workspace/mobinha_license/src/morai_ws/devel/lib/python3/dist-packages/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/workspace/mobinha_license/src/morai_ws/devel/lib/python3/dist-packages/morai_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/workspace/mobinha_license/src/morai_ws/build/MORAI-ROS_morai_msgs/catkin_generated/installspace/morai_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs/cmake" TYPE FILE FILES "/workspace/mobinha_license/src/morai_ws/build/MORAI-ROS_morai_msgs/catkin_generated/installspace/morai_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs/cmake" TYPE FILE FILES
    "/workspace/mobinha_license/src/morai_ws/build/MORAI-ROS_morai_msgs/catkin_generated/installspace/morai_msgsConfig.cmake"
    "/workspace/mobinha_license/src/morai_ws/build/MORAI-ROS_morai_msgs/catkin_generated/installspace/morai_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/morai_msgs" TYPE FILE FILES "/workspace/mobinha_license/src/morai_ws/src/MORAI-ROS_morai_msgs/package.xml")
endif()

