##purpose
#for reprap MARLIN firmware and others which have an adjustable acceleration
#you want to find the highest acceleration value the positional gantry can complete this test without showing any behaviors that might sacrifice print quality (i.e. vibration, positional overshoot, poor cornering)
#this will become the machine's default acceleration, allowing for smoother mechanical movements
 
#1. adjust the machine parameters below based on the specifics of your machine
#2. set a known good travel speed in the inputs
#3. decide on a range of acceleration value to test. y_acc_i is the initial value and y_acc_f being the final value.
#4. set the incremental value to increase acceleration by for each test movement routine
#5. adjust lat_movements to control how fine or coarse the movement routine is
#6. run the script with python and write to a .gcode file  (terminal: python calibration-y-acc.py > acceleration-test.gcode)
#7. run the exported gcode in host software and take note of which routine increment starts to create excessive vibrations or other unwanted mechanical movements
#8. (optional) repeat while adjusting "increments" each time to get a more precise reading

##machine parameters
z_max = 100.0; #mm length of z axis to be tested (make sure value is smaller than total height to avoid hitting platform)
x_center = 0; #x coordinates of center of platform
y_center = 0; #y coordinates of center of platform

##inputs
speed_t = 200; #(mm/s) fixed travel speed
z_acc_i = 6000; #(mm/s/s)
z_acc_f = 14000; #(mm/s/s)
increments = 500; #(mm/s/s)incremental increase in acceleration
lat_movements = 10; #(#)total number of movements parallel to the axis being tested for each routine


#custom startup gcode commands
print "G28"

speed_t_min = speed_t * 60
stepsize = z_max/(lat_movements/2)

#go to z_max
for n in range (0, ((z_acc_f-z_acc_i)/increments)+1):
	print "M201" + " " + "Z" + str(z_acc_i + n*increments)
	for i in range(0, lat_movements/2):
		print "G1"+" "+"Z"+ str(z_max-i*stepsize)+" "+"F"+str(speed_t_min)
		print "G1"+" "+"Z"+ str(stepsize+i*stepsize)+" "+"F"+str(speed_t_min)
