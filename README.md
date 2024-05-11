<p align="center">
  <img height="662" src="/docs/image/Web_Photo_Editor.jpg"/>
</p>

## What is SaMoVi ?

mobinha is a self driving system implementation project.
mobinha performs the functions of Map-based self driving, Adaptive Cruise Control (ACC), Lane Keeping System (LKS)..

Directory Structure
-----
    .
    ├── common              # Library like functionality we've developed here
    ├── docs                # Documentation
    ├── scripts             # system starts/stops script files
    ├── tools               # Unit tests, system tests, and a simulator
    └── selfdrive           # Code needed to drive the car
        ├── manager         # Daemon that starts/stops all other daemons as needed
        ├── car             # Car specific code to read states and control actuators
        ├── planning        
        ├── control 
        └── perception
        
# SaMoVi
copies from mobinha and reconstruct it

1. docker load download from https://drive.google.com/file/d/14u_F9XC88bxR0FuWYeuI-NzAjsTByHFw/view?usp=drive_link in /src/docker or build Dockerfile with build_docker.sh with chaning docker image name

2. and run docker with run_container.sh and start docker after first time with start_container.sh

3. In container pip3 install -r requirements.txt and install other contents in requirements.txt as comments.

4. catkin_make the src/ and src/morai_ws/src or refer https://github.com/MORAI-Autonomous/MORAI-ROS_morai_msgs

5. Run the system with command runmob
