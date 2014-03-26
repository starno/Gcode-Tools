##purpose
#for reprap MARLIN firmware and others which have an adjustable parameter called "jerk"
#you want to find the maximum speed in which your gantry can move back and forth without the need for acceleration
#this will become the default minimum speed whenever changing directions, saving time by avoiding a deceleration to zero each time
 
#1. edit your firmware parameters so that acceleration and jerk are turned OFF
#2. adjust the inputs below based on the specifics of your machine
#3. run the script with python and write to a .gcode file
#4. run the gcode in host software and take note of when the jerk speed starts to create excessive vibrations or other unwanted mechanical movements
#5. (optional) repeat while adjusting "increments" each time to get a more precise maximum acceptable jerk speed


##inputs
travel_distance = 10.0; #mm
x_center = 0; #x coordinates of center of platform
y_center = 0; #y coordinates of center of platform
z_height = 50; #z coordinates to perform test
speed_i = 10; #(mm/s) starting jerk speed
speed_f = 20; #(mm/s) final jerk speed
z_v = 1000; #(mm/min) default speed of z-axis
increments = 2; #(mm/s)incremental increase in speed
iterations = 5; #(#)number of movements back and forth

#custom startup gcode commands
print "G28"

speed_i_min = speed_i * 60
speed_f_min = speed_f * 60
#go to z_height
print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+str(z_v)

#begin jerk movements
for n in range (0,((speed_f_min - speed_i_min)/(increments*60))+1):
	for i in range (0,iterations):
		print "G1"+" "+"X"+ str(travel_distance) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		
	for i in range (0,iterations):
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(travel_distance) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
	
	for i in range (0,iterations):
		print "G1"+" "+"X"+ str(-travel_distance) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		
	for i in range (0,iterations):
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(-travel_distance) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
		print "G1"+" "+"X"+ str(x_center) +" "+"Y"+ str(y_center) +" "+"Z"+ str(z_height) +" "+"F"+ str(speed_i_min + increments*n*60)
									
#custom end gcode commands	
print "G28"	
