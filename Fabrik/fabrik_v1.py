#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
from F_Arm import *
from std_msgs.msg import String
import math

new_massage = False

max_reach = 74.6831

joy_msg = JOY()


global X, Y, Z

X = 0
Y = 0
Z = 0


def joy_callback(msg):
    #new_massage = True
    global X, Y, Z
    X += msg.axes[3] * 0.10
    Y += msg.axes[0] * 0.10
    Z += msg.axes[1] * 0.10
    

    


if __name__ == "__main__":
    my_joints = []
    my_joints.append([0.0,0.0,7.0])
    my_joints.append([0.0,0.0,33.5])
    my_joints.append([27.3,0.0,26.5])
    my_joints.append([47.3,0.0,26.5])
    #arm = F_ARM()

    link_lengths = [26.5, 28.1831, 20]
    REACH = 74.6831

    

    rospy.init_node('fabrik')
    joint_1_publisher = rospy.Publisher('/joint__1_controller/command', F64, queue_size=10)
    joint_2_publisher = rospy.Publisher('/joint__2_controller/command', F64, queue_size=10)
    joint_3_publisher = rospy.Publisher('/joint__3_controller/command', F64, queue_size=10)
    joint_4_publisher = rospy.Publisher('/joint__4_controller/command', F64, queue_size=10)
    joint_5_publisher = rospy.Publisher('/joint__5_controller/command', F64, queue_size=10)
    joint_6_publisher = rospy.Publisher('/joint__6_controller/command', F64, queue_size=10)
    #right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10)
    #left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10)
    
    rospy.Subscriber('joy', Joy, joy_callback)

    rate = rospy.Rate(150)

    count = 0
    first_run = True

    while not rospy.is_shutdown():

        
        if first_run:
            X = 0
            Y = 0
            Z = 0
            joint_1_angles = 0.0
            first_run = False

       
        new_end_point_pos = [47.3, 0.0, 26.5]
        new_end_point_pos[0] = new_end_point_pos[0] + X
        new_end_point_pos[1] = new_end_point_pos[1] + Y
        new_end_point_pos[2] = new_end_point_pos[2] + Z

        rospy.loginfo_throttle(2,"Target X = %s Y = %s Z= %s" %(new_end_point_pos[0], new_end_point_pos[1], new_end_point_pos[2]))

        joint_1_angle_differance = (-1.0) * joint_1_angles

        referance_coord_point = [4,0,0]
        proj_joint_1 = [new_end_point_pos[0], new_end_point_pos[1], 0.0]       
        joint_1_angles = angle_of_vectors(proj_joint_1, referance_coord_point)

        if proj_joint_1[1] < 0:
            joint_1_angles = joint_1_angles * (-1)
        rospy.loginfo_throttle(2,"Joint_1 angle: %s" %joint_1_angles)
        
        joint_1_angle_differance += joint_1_angles

        rotate_on_xy(my_joints[0], joint_1_angle_differance)
        rotate_on_xy(my_joints[1], joint_1_angle_differance)
        rotate_on_xy(my_joints[2], joint_1_angle_differance)
        rotate_on_xy(my_joints[3], joint_1_angle_differance)

        FABRIK_algorithm(my_joints, link_lengths, new_end_point_pos, REACH)

        
        joint_5_angle = find_angle(my_joints[2], my_joints[1], my_joints[3], joint_1_angles)
        joint_3_angle = find_angle(my_joints[1], my_joints[0], my_joints[2], joint_1_angles)
        joint_2_angle = find_angle(my_joints[0], [0.0,0.0,0.0], my_joints[1], joint_1_angles)

        joint_angles = [joint_1_angles, 180.0 - joint_2_angle, 90.0 - (joint_3_angle + 14.38138), 0.0, (joint_5_angle + 75.61862) - 270.0]

        joint1_last = (joint_angles[0]*math.pi)/180
        joint2_last = (joint_angles[1]*math.pi)/180
        joint3_last = (joint_angles[2]*math.pi)/180
        joint4_last = (joint_angles[3]*math.pi)/180
        joint5_last = (joint_angles[4]*math.pi)/180
        joint6_last = 0.0
        
        joint_1_publisher.publish(joint1_last)
        joint_2_publisher.publish(joint2_last)
        joint_3_publisher.publish(joint3_last)
        joint_4_publisher.publish(joint4_last)
        joint_5_publisher.publish(joint5_last)
        joint_6_publisher.publish(joint6_last)

        rate.sleep()
        
    




