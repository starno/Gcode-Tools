##purpose
#for reprap MARLIN firmware and others which have an adjustable acceleration
#you want to find the highest acceleration value the positional gantry can complete this test without showing any behaviors that might sacrifice print quality (i.e. vibration, positional overshoot, poor cornering)
#this will become the machine's default acceleration, allowing for smoother mechanical movements
 
#1. adjust the machine parameters below based on the specifics of your machine
#2. set a known good travel speed in the inputs
#3. decide on a range of acceleration value to test. x_acc_i is the initial value and x_acc_f being the final value.
#4. set the incremental value to increase acceleration by for each test movement routine
#5. adjust lat_movements to control how fine or coarse the movement routine is
#6. run the script with python and write to a .gcode file  (terminal: python acceleration.py > acceleration-test.gcode)
#7. run the exported gcode in host software and take note of which routine increment starts to create excessive vibrations or other unwanted mechanical movements
#8. (optional) repeat while adjusting "increments" each time to get a more precise reading

##machine parameters
x_max = 120.0; #mm total length of x axis
y_max = 120.0; #mm total length of y axis
x_center = 0; #x coordinates of center of platform
y_center = 0; #y coordinates of center of platform
z_height = 50; #z coordinates to perform test

##inputs
speed_t = 160; #(mm/s) fixed travel speed
x_acc_i = 700; #(mm/s/s)
x_acc_f = 1100; #(mm/s/s)
z_v = 1000; #(mm/min) default speed of z-axis
increments = 100; #(mm/s/s)incremental increase in acceleration
lat_movements = 20; #(#)total number of movements parallel to the axis being tested for each routine



#custom startup gcode commands
print "G28"

speed_t_min = speed_t * 60

#go to z_height
print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height)+" "+"F"+str(z_v)
#go to bottom left of print area
print "G1"+" "+"X"+ str((-x_max/2)+x_center) +" "+"Y"+ str((y_center)) +" "+"F"+str(speed_t_min)
print "G1"+" "+"X"+ str((-x_max/2)+x_center) +" "+"Y"+ str((-y_max/2)+ y_center)


#start routine
x_stepsize = x_max/(lat_movements/2)
y_stepsize = y_max/(lat_movements)
for n in range(0, ((x_acc_f-x_acc_i)/increments)+1):
	print "M400"
        print "M201" + " " + "X" + str(x_acc_i + n*increments) + " " + "Y" + str(x_acc_i + n*increments) + " " + "Z" + str(x_acc_i + n*increments)
        for i in range(0, lat_movements/2):
                print "G1"+" "+"X"+ str((x_max/2)+x_center-(i*x_stepsize))
                print "G1"+" "+"Y"+ str((-y_max/2)+y_center+(i*y_stepsize+(i+1)*y_stepsize))
                print "G1"+" "+"X"+ str((-x_max/2)+x_center+((i+1)*x_stepsize))
        	print "G1"+" "+"Y"+ str((-y_max/2)+y_center+(i*y_stepsize+(i+2)*y_stepsize))
        print "G1"+" "+"X"+ str((-x_max/2)+x_center) +" "+"F"+str(speed_t_min)
        print "G1"+" "+"X"+ str((-x_max/2)+x_center) +" "+"Y"+ str((-y_max/2)+ y_center)
