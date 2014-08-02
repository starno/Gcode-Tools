temp = 60; #deg C, temperature of platform
cool_temp = 50; #deg C, temperature of cooled platform
cycles = 10; #number of heating cycles

for i in range(0,cycles):
	print ";Heated " + str(i+1) + " times";
	print "M190 R" + str(temp) + ";";
	print "M190 R" + str(cool_temp) + ";";
	