#!/usr/bin/env python

import rospy
import math
import serial
import rosparam
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray

global axes
axes = ["0000","0000","0000","0000","0000","0000"]




global serialString 
serialString = "/dev/ttyUSB0"

global ser
#ser = serial.Serial(port=serialString, baudrate=int(115200), parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)




def callback_send(data):
	#rospy.loginfo(data.data)
	global ser
	angle_to_string_V2(0,data.data[0])
	angle_to_string_V2(1,data.data[1])
	angle_to_string_V2(2,data.data[2])
	angle_to_string_V2(3,data.data[3])
	angle_to_string_V2(4,data.data[4])
	velocity_to_string(5, data.data[5])
	final_message = create_final_message_V2()
	rospy.loginfo(final_message)
	serial_pub.publish(final_message)
	#ser.write(final_message+"\n")

def velocity_to_string(axis_index, velocity):
	global axes
	if velocity >= 0:
		string_velocity = "1"
	elif velocity < 0:
		string_velocity = "0"
	
	print("Axis: "+ str(axis_index) + " degrees: "+ str(velocity))
	velocity = int(abs(velocity))
	string_velocity = string_velocity + "0"*(3-len(str(velocity))) + str(velocity)
	print(string_velocity)
	axes[axis_index] = string_velocity

def angle_to_string_V2(axis_index,radian):
	global axes
	degrees = int(180*radian/math.pi)
	if degrees >= 0:
		string_angle = "1"
	elif degrees < 0:
		string_angle = "0"
	print("Axis: "+ str(axis_index) + " degrees: "+ str(degrees))
	degrees = abs(degrees)
	string_angle = string_angle + "0"*(3-len(str(degrees))) + str(degrees)
	print(string_angle)
	axes[axis_index] = string_angle

def create_final_message_V2():
	global axes
	final_message = "S" + 8*"0"
	for i in axes:
		final_message += i
	final_message = final_message + 20*"0" + "2F"
	return final_message
	




if __name__ == '__main__':

	
	###ser = serial.Serial(....) #serial acilir



	rospy.init_node('serial_arm_node')
	rospy.Subscriber('/axis_states/send',Float64MultiArray,callback_send)
	#rospy.Subscriber('encoder',String,callback_enc)
	serial_pub = rospy.Publisher('rover_serial/arm',String,queue_size=50)
	axis_pub = rospy.Publisher('/axis_states/get',Float64MultiArray,queue_size=50)
	
	rate = rospy.Rate(150)

	while not rospy.is_shutdown():

		#print('________')
		'''if control:
			final_message = create_final_message()
			rospy.loginfo(final_message)
			serial_pub.publish(final_message)'''
		#message = Float64MultiArray(data=current_enc_thetas)
		#print(current_enc_thetas)
		#print(axes)
		#axis_pub.publish(message)
		rate.sleep()





