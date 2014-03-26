#!/usr/bin/python


#Change Temperature Settings in Pre-existing Gcode Files

# Run python script specifying the input gcode location, -i, and at least one of four temperature arguments: extruder, et; first layer extruder, et1; build platform, bt; first layer build platform, bt1;
 
#$ python tempchange.py -i <gcode location> -et1-230 -et-220



import argparse
import re
import sys


parser = argparse.ArgumentParser(description='Change the printing temperatures within a gcode without having to slice the file again ')

parser.add_argument('-i', '--input', type=str, default="",
                    help='The location of the gcode file to run through the script')
parser.add_argument('-et', '--etemp', type=float,
                    help='The specified extruder temperature in C')
parser.add_argument('-et1', '--etemp1', type=float,
                    help='The specified extruder temperature for the first layer in C')
parser.add_argument('-bt', '--btemp', type=float,
                    help='The specified build platform temperature in C')
parser.add_argument('-bt1', '--btemp1', type=float,
                    help='The specified build platform temperature for the first layer in C')


args=parser.parse_args()


filename = args.input;
if (filename == ""):
	parser.print_help()
	sys.exit(-1)
newfilename = re.sub(".gcode", "-new.gcode", args.input)
f = open(filename, 'r')
g = open(newfilename, 'w')


##set variables
bed_temp = args.btemp;
first_layer_bed_temp = args.btemp1
extruder_temp = args.etemp
first_layer_extruder_temp = args.etemp1


#Find first bed and extruder temperature instances, replace if temperature argument is specified
first190seen=0
first104seen=0


for l in f:
    if "M190" in l and "S0" not in l:
        if first190seen == 0:
            if first_layer_bed_temp is not None:
              l= re.sub("M190 S.*;", 'M190 S' + str(first_layer_bed_temp) + ' ;', l, 1)
            first190seen += 1
        else:
            if bed_temp is not None:
              l = re.sub("M190 S.*;", 'M190 S' + str(bed_temp) + ' ;', l)
    elif  "M140" in l and "S0" not in l:
        if bed_temp is not None:
            l= re.sub("M140 S.*;", 'M140 S' + str(bed_temp) + ' ;', l)
    elif "M104" in l and "S0" not in l:
        if first104seen == 0:
            if extruder_temp is not None:
               l= re.sub("M104 S.*;", 'M104 S' + str(first_layer_extruder_temp) + ' ;', l, 1)
            first104seen += 1
        else:
            if first_layer_extruder_temp is not None:
              l= re.sub("M104 S.*;", 'M104 S' + str(extruder_temp) + ' ;', l)
    elif  "M109" in l and "S0" not in l:
        if first_layer_extruder_temp is not None:
            l= re.sub("M109 S.*;", 'M109 S' + str(first_layer_extruder_temp) + ' ;', l)
    g.write(l)
    
    
g.flush()
g.close()