#This script uses the end effector mounted toolhead to push buttons on a euclid HBP (euclid-3d.com/hbp) or similar device 
#   and log diagnostic data into a csv file that can help determine the sources of positional error of the deltabot 
#	kinematic design and/or assembly.

#Prior Requirements: Delta Marlin firmware which has defined M33 & M34 Platform button poking routines 
#   (i.e. https://github.com/starno/Marlin)


###Directions###
#1. Flash compatible delta firmware (uses M33 & M34 mcodes)
#2. Verify button coordinates particular to your machine and edit locations in the Hardware Preferences below
#3. Edit the number of datapoints to collect, platform temp as desired
#4. Toggle which routines to be included (True = run  False = dont run)
#5. Connect machine to computer via USB, change log file name and serial port as needed
#6. Point terminal to script directory, type "python delta-diagnostic-test.py" to run
#7. Open log file and import as CSV into excel or similar application to plot deviation of each routine
#8. Compare results of the different routines with the Zmotion routines to determine what is the biggest source of your 
#		deltabot's positional error


##########Inputs##########

##Hardware Preferences
ZTOWER_X = -4; #x-coordinate of Ztower button(mm) 
ZTOWER_Y = 97; #y-coordinate of Ztower button(mm)
XTOWER_X = -85; #x-coordinate of Xtower button(mm)
XTOWER_Y = -42.5; #y-coordinate of Xtower button(mm)
YTOWER_X = 77.5; #x-coordinate of Ztower button(mm)
YTOWER_Y = -43; #x-coordinate of Ztower button(mm)
HOVER_HEIGHT = 5; #height above button to begin small movements(mm)

##Testing Preferences
datapoints = 300; #sample size for each routine
platform_temp = 125; #temp of platform for testing routine while heated (degC)
SPEED = 2000; #mm/min travel speed

##Testing Routines
ThreeD_motion = True; #add routine that uses movements on all axes
ThreeD_motion_heated = True; #add routine that uses movements on all axes while platform is heated
Z_motion = True; #add routine that uses movements on cartesian z-axis only
Z_motion_heated = True; #add routine that uses movements on cartesian z-axis only while platform is heated
include_homing = False; #add homing operation between each button poking operation

##Logging Preferences
log_filename = 'delta-diagnostic-test.txt';
serial_port = '/dev/tty.usbmodem1411';
baud_rate = 115200;


##########Script##########

import serial
import time

port = serial.Serial(serial_port, baud_rate)
time.sleep(3)

port.write('G28\n')

log=open(log_filename, 'a')  #append mode

if ThreeD_motion == True:
	for i in range(0, datapoints):
		port.write('M33\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True
			
		if include_homing == True:
			port.write('G28\n')

if Z_motion == True:
	for i in range(0, datapoints):
		port.write('G1 X' + str(ZTOWER_X) + ' Y' + str(ZTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True
			
	for i in range(0, datapoints):
		port.write('G1 X' + str(XTOWER_X) + ' Y' + str(XTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')
	
		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True		

	for i in range(0, datapoints):
		port.write('G1 X' + str(YTOWER_X) + ' Y' + str(YTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')
	
		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True
			
			
#######Heated Routines#############

if ThreeD_motion_heated == True:
	port.write('M190 S' + str(platform_temp) + '\n')	
	for i in range(0, datapoints):
		port.write('M33\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True
				
		if include_homing == True:
			port.write('G28\n')	
			
	port.write('M190 S0\n')		


if Z_motion_heated == True:
	port.write('M190 S' + str(platform_temp) + '\n')	
	for i in range(0, datapoints):
		port.write('G1 X' + str(ZTOWER_X) + ' Y' + str(ZTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True
			
	port.write('M190 S0\n')	
	
	port.write('M190 S' + str(platform_temp) + '\n')	
	for i in range(0, datapoints):
		port.write('G1 X' + str(XTOWER_X) + ' Y' + str(XTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True

	port.write('M190 S0\n')		

	port.write('M190 S' + str(platform_temp) + '\n')	
	for i in range(0, datapoints):
		port.write('G1 X' + str(YTOWER_X) + ' Y' + str(YTOWER_Y) + ' Z' + str(HOVER_HEIGHT) + ' F' + str(SPEED) + '\n')
		port.write('M34\n')

		finished = False
		while not finished:
			response = port.readline()
			print response,
        
			if response.startswith('XYZ'):
				log.write(response[4:])
				log.flush()
				finished = True

	port.write('M190 S0\n')	
	
port.write('G28\n')	
				
log.close()
port.close()