# Autonomous_navigation_ros
2D autonomous navigation of two wheel differential drive robot using ros navigation package.
Given a point in the map, the robot can autonomously navigate to the goal point avoiding the static and dynamic obstracles in between.

## Hardware used
Intel R200 realsense camera - To collect the depth information of the image.

Intel UP board - For processing the slam package.

Arduino mega - used to publish odomerty information to board and to provide commands to move chassis.

Dc motor with encoder - Used to collect odometry infomation and to move chassis. 

### Installing
Few ros packages and dependiencies must be installed before running the above packages.

ros navigation package(for kinetic)
```
sudo apt-get install ros-kinetic-navigation
```

ros serial arduino(for kinetic)
```
sudo apt-get install ros-kinetic-rosserial-arduino
sudo apt-get install ros-kinetic-rosserial
```

Octomap, ROS integration, and octomap_server(for kinetic)
```
sudo apt-get install ros-kinetic-octomap ros-kinetic-octomap-mapping
```


## Running the tests

first launch 
```
roslaunch Ajit_mapping slam.launch
```
second launch 
```
roslaunch humanoid_chassis new_rviz.launch
```

At this point, Rviz would be launched on your display with robot model loaded. Using the 2D nav command the goal point 
where the robot has to navigate should be given. Within few seconds the local and global path will be produce which robot 
would follow and the reach the goal point.

## Images 



