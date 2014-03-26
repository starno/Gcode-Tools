#Purpose
#for testing MKX extruder designs, finding the limits of retraction length to quantify effectiveness of hotend prototype geometry.
#define the range of retraction distance to test, ret_l_min and ret_l_max, set the increment to test within the range and the total number of cycles each. 

#Extruder Config
temperature = 170.0; #(degC) extrusion temperature (170-200 for PLA, 220-250 for ABS)
ext_speed = 20.0; #(mm/min) extrusion speed (default = 100)
ret_speed = 40.0; #(mm/s) retraction speed (default = 40)

#Testing Parameters
ret_l_min = 2.0; #(mm) min length of retraction
ret_l_max = 2.1; #(mm) max length of retraction
increment = 0.1; #(#) step size of each iteration
ext_l = 0.25; #(mm) length of extrusion based on filament input
cycles = 100.0; #(#) number of cycles to extrude for each incremental retraction length (1000.0 minimum for good diagnosis)

#conversions
iterations = (ret_l_max - ret_l_min) / increment;
ret_speed_F = ret_speed * 60.0

#custom startup gcode commands
print "G92 ; use absolute coordinates"
print "G28"
print "G1 X0 Y0 Z100 F1500"
print "G21 ; set units to millimeters"
print "M104 S" + str(temperature) + " ; set temperature"
print "M109 S" + str(temperature) + " ; wait for temperature to be reached"
print "G92 E0"
print "G91 ; use relative coordinates"


print "G1 F" + str(ext_speed) + " E10.0"
for n in range(0, int(iterations)+1):
	for i in range(0, int(cycles)):	
		print "G1 F" + str(ext_speed) + " E" + str(ext_l)
		print "G1 F" + str(ret_speed_F) + " E-" + str(ret_l_min + increment*n)
		print "G1 F" + str(ret_speed_F) + " E" + str(ret_l_min + increment*n)
print "G1 F" + str(ext_speed) + " E" + str(ext_l)

