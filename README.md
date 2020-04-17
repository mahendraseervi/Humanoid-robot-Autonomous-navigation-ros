# Autonomous_navigation_ros
2D autonomous navigation of two wheel differential drive robot using ros navigation package.
Given a point in the map, the robot can autonomously navigate to the goal point avoiding the static and dynamic obstracles in between.

## Hardware used
Intel R200 realsense camera - To collect the depth information of the image.

Intel UP board - For processing the slam package.

Arduino mega - used to publish odomerty information to UP board and to provide commands to move chassis.

Dc motor with encoder - Used to collect odometry infomation and to move chassis. 

## Installing
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


## Running the package

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

## Working youtube Video Link:
https://www.youtube.com/embed/kuIxMKZp3ro

## For more information:
https://mahendraseervi.github.io/project%20humanoid.html

## Images: 
![screenshot from 2018-04-24 09-21-06](https://user-images.githubusercontent.com/21152256/39403443-033d025c-4b9a-11e8-8583-0e2be3dfcd1f.png)

![screenshot from 2018-04-24 09-20-49](https://user-images.githubusercontent.com/21152256/39403444-0bae8ab4-4b9a-11e8-8c42-588eec430b3f.png)

![rosgraph](https://user-images.githubusercontent.com/21152256/39403445-0ebfcee8-4b9a-11e8-927b-b8c08df71f89.png)

![img_20180427_210758_475](https://user-images.githubusercontent.com/21152256/39403447-15b2f93c-4b9a-11e8-9550-34e56bdd853a.jpg)

