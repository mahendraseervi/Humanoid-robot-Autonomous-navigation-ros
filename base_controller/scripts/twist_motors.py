#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from numpy import interp

left = 0.0
right = 0.0
w = 0.32  # distance between wheels in meters


def callback(msg):
    global vx, vy, vr, pub
    ############### to find the speed value ############################
    # vx = msg.linear.x * 100
    # vz = msg.angular.z * 100
    #
    # if(vx != 0):
    #     if(vx > 0):
    #         pub.publish("w,"+str(vx))
    #     elif(vx < 0):
    #         vx = abs(vx)
    #         pub.publish("s,"+str(vx))
    #
    # elif(vz != 0):
    #     if(vz > 0):
    #         pub.publish("a,"+str(vz))
    #     elif(vx < 0):
    #         vz = abs(vz)
    #         pub.publish("d,"+str(vz))
    #
    # else:
    #     pub.publish("c,0")

    ###################   values found ##########################
        # max pwm = 40   min pwm = 30
        # max linear vel = 0.26 min linear vel = 0.17

        # max pwm = 43   min pwm = 37
        # max angular vel = 0.92  min angular vel = 0.55

    ################   to run navigation ########################
    if vz > 0.92 and vz < 5 :
        vz = 0.92

    if vz < 0.55 and vz > 0.4 :
        vz = 0.55


    if vz < -0.4 and vz > -0.55:
        vz = -0.55
        print("wrapped")

    if vz < -0.92 and vz > -2:
        vz = -0.92


    if((vx != 0) or (vz != 0)):
        if(vx != 0):
            if (vx >= 0.17 and vx <= 0.26):
                vx = int(interp(vx,[0.17,0.26],[26,56]))
                pub.publish("w,"+str(vx))
            elif(vx <= -0.17 and vx >= -0.26):
                vx = int(interp(vx,[-0.26,-0.17],[56,26]))
                pub.publish("s,"+str(vx))

        if(vz != 0):
            if(vz >= 0.55 and vz <= 0.92):
                vz = int(interp(vz,[0.55,0.92],[25,30]))
                pub.publish("a,"+str(vz))
            elif(vz <= -0.55 and vz >= -0.92):
                vz = int(interp(vz,[-0.92,-0.55],[30,25]))
                pub.publish("d,"+str(vz))

    else:
        pub.publish("c,0")

    print(vz)
    ##################################################################33

if __name__ == '__main__':
    rospy.init_node('twist_motors', anonymous=True)
    pub = rospy.Publisher('base_cmd', String, queue_size=10)
    rospy.Subscriber("cmd_vel", Twist, callback)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        rate.sleep()
