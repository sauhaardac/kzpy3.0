#!/usr/bin/env python

"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""
try:

	########################################################
	#          CAFFE SETUP SECTION
    import torch
    torch.set_default_tensor_type('torch.FloatTensor')
	from kzpy3.utils import *
	from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
	import cv2
	os.chdir(home_path) # this is for the sake of the train_val.prototxt
	#import run_params
	#from run_params import *
	import kzpy3.teg2.car_run_params
	from kzpy3.teg2.car_run_params import *

	#solver_file_path = opjh("kzpy3/caf5/z2_color/solver_live.prototxt")
	#weights_file_path = opjh('kzpy3/caf5/z2_color/z2_color.caffemodel') #
	def setup_solver():
        net = Z2Color().cuda()
		return net
	solver = setup_solver()
	if weights_file_path != None:
		print "loading " + weights_file_path
        save_data = torch.load(args.resume)
        solver.load_state_dict(save_data['net'])
	#
	########################################################


	########################################################
	#          ROSPY SETUP SECTION
	import roslib
	import std_msgs.msg
	import cv2
	from cv_bridge import CvBridge,CvBridgeError
	import rospy
	from sensor_msgs.msg import Image
	bridge = CvBridge()
	rospy.init_node('listener',anonymous=True)

	left_list = []
	right_list = []
	A = 0
	B = 0
	state = 0
	previous_state = 0
	state_transition_time_s = 0

	def state_callback(data):
		global state, previous_state
		if state != data.data:
			if state in [3,5,6,7] and previous_state in [3,5,6,7]:
				pass
			else:
				previous_state = state
		state = data.data
	def right_callback(data):
		global A,B, left_list, right_list, solver
		A += 1
		cimg = bridge.imgmsg_to_cv2(data,"bgr8")
		if len(right_list) > 5:
			right_list = right_list[-5:]
		right_list.append(cimg)
	def left_callback(data):
		global A,B, left_list, right_list
		B += 1
		cimg = bridge.imgmsg_to_cv2(data,"bgr8")
		if len(left_list) > 5:
			left_list = left_list[-5:]
		left_list.append(cimg)
	def state_transition_time_s_callback(data):
		global state_transition_time_s
		state_transition_time_s = data.data


	GPS2_lat = -999.99
	GPS2_long = -999.99
	GPS2_lat_orig = -999.99
	GPS2_long_orig = -999.99
	def GPS2_lat_callback(msg):
		global GPS2_lat
		GPS2_lat = msg.data
	def GPS2_long_callback(msg):
		global GPS2_long
		GPS2_long = msg.data

	camera_heading = 49.0
	def camera_heading_callback(msg):
		global camera_heading
		c = msg.data
		#print camera_heading
		if c > 90:
			c = 90
		if c < -90:
			c = -90
		c += 90
		c /= 180.
		
		c *= 99

		if c < 0:
			c = 0
		if c > 99:
			c = 99
		c = 99-c
		camera_heading = int(c)

	##
	########################################################

	import thread
	import time


	rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
	rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
	rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32,state_callback)
	rospy.Subscriber('/bair_car/state_transition_time_s', std_msgs.msg.Int32, state_transition_time_s_callback)
	steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
	motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
	model_name_pub = rospy.Publisher('/bair_car/model_name', std_msgs.msg.String, queue_size=10)
	#rospy.Subscriber('/bair_car/GPS2_lat', std_msgs.msg.Float32, callback=GPS2_lat_callback)
	#rospy.Subscriber('/bair_car/GPS2_long', std_msgs.msg.Float32, callback=GPS2_long_callback)
	#rospy.Subscriber('/bair_car/GPS2_lat_orig', std_msgs.msg.Float32, callback=GPS2_lat_callback)
	#rospy.Subscriber('/bair_car/GPS2_long_orig', std_msgs.msg.Float32, callback=GPS2_long_callback)
	#rospy.Subscriber('/bair_car/camera_heading', std_msgs.msg.Float32, callback=camera_heading_callback)


	ctr = 0


	#from kzpy3.teg2.global_run_params import *

	t0 = time.time()
	time_step = Timer(1)
	caffe_enter_timer = Timer(2)
	folder_display_timer = Timer(30)
	git_pull_timer = Timer(60)
	reload_timer = Timer(10)
	#verbose = False
	
	while not rospy.is_shutdown():
		if state in [3,5,6,7]:
			if (previous_state not in [3,5,6,7]):
				previous_state = state
				caffe_enter_timer.reset()
			if not caffe_enter_timer.check():
				#print caffe_enter_timer.check()
				print "waiting before entering caffe mode..."
				steer_cmd_pub.publish(std_msgs.msg.Int32(49))
				motor_cmd_pub.publish(std_msgs.msg.Int32(49))
				time.sleep(0.1)
				continue
			else:
				if len(left_list) > 4:
					l0 = left_list[-2]
					l1 = left_list[-1]
					r0 = right_list[-2]
					r1 = right_list[-1]

                    # Camera Data input
                    camera_data = torch.FloatTensor()

                    for c in range(3):
                        raw_input_data = torch.cat((torch.from_numpy(l0[:,:,0]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(l1[:,:,0]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r0[:,:,0]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r1[:,:,0]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(l0[:,:,1]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(l1[:,:,1]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r0[:,:,1]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r1[:,:,1]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(l0[:,:,2]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(l1[:,:,2]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r0[:,:,2]).float(), camera_data), 2)
                        raw_input_data = torch.cat((torch.from_numpy(r1[:,:,2]).float(), camera_data), 2)

                    camera_data = camera_data.cuda()  # CUDA data before maniupation
                    camera_data /= 255.
                    camera_data = torch.transpose(camera_data, 0, 2)
                    camera_data = torch.transpose(camera_data, 1, 2)
						
                    metadata = torch.FloatTensor()                        
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(Racing), metadata), 0)
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(0), metadata), 0)
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(Follow), metadata), 0)
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(Direct), metadata), 0)
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(Play), metadata), 0)
                    torch.cat((torch.FloatTensor(1, 13, 26).fill_(Furtive), metadata), 0)

                    output = solver(camera_data, metadata) * 100

                    caf_steer, caf_motor = torch.chunk(output, 2)  # Get caf_steer and caf_motor

					"""
					if caf_motor > 60:
						caf_motor = (caf_motor-60)/39.0*10.0 + 60
					"""

					caf_motor = int((caf_motor-49.) * motor_gain + 49)
					caf_steer = int((caf_steer-49.) * steer_gain + 49)



					if caf_motor > 99:
						caf_motor = 99
					if caf_motor < 0:
						caf_motor = 0
					if caf_steer > 99:
						caf_steer = 99
					if caf_steer < 0:
						caf_steer = 0

					if verbose:
						print caf_motor,caf_steer,motor_gain,steer_gain,state
					
					if state in [3,6]:			
						steer_cmd_pub.publish(std_msgs.msg.Int32(caf_steer))
					if state in [6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(caf_motor))

		else:
			pass

		if state == 4 and state_transition_time_s > 30:
			print("Shutting down because in state 4 for 30+ s")
			unix('sudo shutdown -h now')
		if time_step.check():
			print(d2s("In state",state,"for",state_transition_time_s,"seconds, previous_state =",previous_state))
			time_step.reset()
			if not folder_display_timer.check():
				print("*** Data foldername = "+foldername+ '***')
		if reload_timer.check():
			#reload(run_params)
			#from run_params import *
			reload(kzpy3.teg2.car_run_params)
			from kzpy3.teg2.car_run_params import *
			model_name_pub.publish(std_msgs.msg.String(weights_file_path))
			reload_timer.reset()

		if git_pull_timer.check():
			unix(opjh('kzpy3/kzpy3_git_pull.sh'))
			git_pull_timer.reset()

except Exception as e:
	print("********** Exception ***********************",'red')
	print(e.message, e.args)
	rospy.signal_shutdown(d2s(e.message,e.args))

