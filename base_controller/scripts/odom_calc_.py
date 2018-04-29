#!/usr/bin/env python
import rospy
import time

from math import sin, cos, pi

from geometry_msgs.msg import Quaternion
# from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
import tf
from std_msgs.msg import Int32, String
import numpy

PI = 3.1415926535897931

enL = 0
enR = 0

oldenL = 0
oldenR = 0

dl = 0.0
dr = 0.0
dt = 0.0

wheelCircumference = (2 * PI * 0.05)  #in meters
wheelDistance = 0.32
encoderResolution = 360

x = 0.0      # distance in coordinate frame (x = straight)
y = 0.0
th = 0.0      # (th = theta)

vx = 0.0     # velocity in coordinate frame
vy = 0.0
vth = 0.0

dx = 0.0      # change in distance
dy = 0.0
dth = 0.0
odomBroadcaster = TransformBroadcaster()
pub = rospy.Publisher('odom', Odometry, queue_size=10)

def odom_pubCallback(data):
    global enL, enR
    ar = data.data.split(',')
    enL = float(ar[0])
    enR = float(ar[1])

def speedCalc(dl, dr, dt):
    global dth
    global dx
    global dy
    global th
    global wheelDistance

    avg_speed = (dl + dr)/2
    dth = ((dl - dr)/((wheelDistance))/1.0) 
    dx = avg_speed * cos(th + dth)
    dy = avg_speed * sin(th + dth)

def odomCalc():
    global enL
    global enR
    global oldenL
    global oldenR
    global last_time
    global current_time
    global count
    global dx
    global dy
    global dth
    global x
    global y
    global th
    global vx
    global vy
    global vth
    global PI
    global encoderResolution
    global wheelCircumference
    print(enL, enR)

    difL = 0
    difR = 0
    current_time = rospy.Time.now()

    if(enL != oldenL):
        difL = enL - oldenL
        oldenL = enL
    if(enR != oldenR):
        difR = enR - oldenR
        oldenR = enR

    dl = ((difL * wheelCircumference)/ encoderResolution)
    dr = ((difR * wheelCircumference)/ encoderResolution)
    dt = (current_time - last_time)
    dt = dt.to_sec()
    # print(current_time , dt)
    # last_time = current_time

    speedCalc(dl, dr, dt)
    vx = dx/dt
    vy = dy/dt
    vth = dth/dt

    x = x + dx
    y = y + dy
    th = th + dth

    if (th > PI):
        th = th -(2 * PI)
    elif(th < -PI):
        th = th + (2 * PI)

    quaternion = Quaternion()
    quaternion.x = 0.0
    quaternion.y = 0.0
    quaternion.z = sin( th / 2 )
    quaternion.w = cos( th / 2 )
    # quaternion.w = 0
    odomBroadcaster.sendTransform(
        (x, y, 0),
        (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
        rospy.Time.now(),
        "base_link",
        "odom"
        )


    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    #set the positions
    odom.pose.pose.position.x = x
    odom.pose.pose.position.y = y
    odom.pose.pose.position.z = 0
    odom.pose.pose.orientation.x = quaternion.x
    odom.pose.pose.orientation.y = quaternion.y
    odom.pose.pose.orientation.z = quaternion.z
    odom.pose.pose.orientation.w = quaternion.w

    #set velocities
    odom.child_frame_id = "base_link"
    odom.twist.twist.linear.x = vx
    odom.twist.twist.linear.y = vy
    odom.twist.twist.angular.z = vth

    pub.publish(odom)
    last_time = current_time


if __name__ == '__main__':
    rospy.init_node('odom_calc', anonymous=True)

    current_time = rospy.Time.now()
    last_time = rospy.Time.now()

    try:
        rospy.Subscriber("odom_pub", String, odom_pubCallback)

        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # print("sadfsd")
            odomCalc()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
