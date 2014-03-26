#Purpose
#Script creates leveling calibration gcode based on build platform size and other machine configurations.  
#All default values are for euclid delta platforms

#Step1: Point terminal to directory containing delta-radius-calibration.py
#Step2: $ python delta-radius-calibration.py to generate calibration scripts.  Type --help to see additional configurable arguments

import argparse
import re
import sys
parser = argparse.ArgumentParser(description='Create gcode files for an easier deltabot calibration procedure')

parser.add_argument('-d', '--diameter', type=float, default= 170.0,
                    help='The overall diameter of the build platform in mm')
parser.add_argument('-eo', '--effector_offset', type=float, default= 40.0,
                    help='The distance from the center of the end effector to the joints on the arms in mm')
parser.add_argument('-nox', '--nozzle_offset_x', type=float, default= 6.0,
                    help='The distance from the center of the end effector to the center of the extruder nozzle in the x-direction only (mm)')
parser.add_argument('-noy', '--nozzle_offset_y', type= float, default= -4.65,
                    help='The distance from the center of the end effector to the center of the extruder nozzle in the y-direction only (mm)')
parser.add_argument('-home', '--homing_speed', type= float, default= 3000.0,
                    help='The speed of homing in mm/min')


args=parser.parse_args()



#Machine Configuration 
build_diameter = args.diameter;  #(mm) diameter of build area
DELTA_EFFECTOR_OFFSET = args.effector_offset;  #(mm) distance from center of effector to one of the arm joints
nozzle_offset_x = args.nozzle_offset_x; #(mm) x distance from nozzle center to machine center axis
nozzle_offset_y = args.nozzle_offset_y; #(mm) x distance from nozzle center to machine center axis
homing_speed = args.homing_speed; #(mm/min) homing speed

#background math
import math
c_radius = (build_diameter - (DELTA_EFFECTOR_OFFSET*2))/2;
Xtower_pointx = -c_radius*math.cos(30*(math.pi/180.0)); 
Xtower_pointy = -c_radius*math.sin(30*(math.pi/180.0));
Ytower_pointx = c_radius*math.cos(30*(math.pi/180.0)); 
Ytower_pointy = -c_radius*math.sin(30*(math.pi/180.0));
Ztower_pointx = 0; 
Ztower_pointy = c_radius;
Center_pointx = 0; 
Center_pointy = 0;


#Create files
cal_x = open('0_cal_xtower.gcode','wb')
cal_y = open('0_cal_ytower.gcode','wb')
cal_z = open('0_cal_ztower.gcode','wb')
cal_c = open('0_cal_center.gcode','wb')

#Xtower
cal_x.write('G28;\n')
cal_x.write((';G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Xtower_pointx, Xtower_pointy,0,homing_speed)) + "; Xtower Calibration Point\n")
cal_x.write('G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Xtower_pointx - nozzle_offset_x, Xtower_pointy - nozzle_offset_y,0,homing_speed) + "; Including extruder offset:(" + str(nozzle_offset_x) + ", " + str(nozzle_offset_y) + ")\n")
cal_x.close()

#Ytower
cal_y.write('G28;\n')
cal_y.write((';G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Ytower_pointx, Ytower_pointy,0,homing_speed)) + "; Ytower Calibration Point\n")
cal_y.write('G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Ytower_pointx - nozzle_offset_x, Ytower_pointy - nozzle_offset_y,0,homing_speed) + "; Including extruder offset:(" + str(nozzle_offset_x) + ", " + str(nozzle_offset_y) + ")\n")
cal_y.close()

#Ztower
cal_z.write('G28;\n')
cal_z.write((';G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Ztower_pointx, Ztower_pointy,0,homing_speed)) + "; Ztower Calibration Point\n")
cal_z.write('G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Ztower_pointx - nozzle_offset_x, Ztower_pointy - nozzle_offset_y,0,homing_speed) + "; Including extruder offset:(" + str(nozzle_offset_x) + ", " + str(nozzle_offset_y) + ")\n")
cal_z.close()

#Center
cal_c.write('G28;\n')
cal_c.write((';G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Center_pointx, Center_pointy,0,homing_speed)) + "; Center Calibration Point\n")
cal_c.write('G1 X%0.3f Y%0.3f Z%0.3f F%0.3f'%(Center_pointx - nozzle_offset_x, Center_pointy - nozzle_offset_y,0,homing_speed) + "; Including extruder offset:(" + str(nozzle_offset_x) + ", " + str(nozzle_offset_y) + ")\n")
cal_c.close()
