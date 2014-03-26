Gcode-Tools
===========
Gcode generating scripts for 3D printers and other similar robots running Marlin firmware.



Acceleration Calibration
========================
-Define machine parameters and incremental acceleration values that will be generated into gcode.
-Watch the machine run through the generated gcode routine and take note of which acceleration iteration starts to negatively affect performance.


Delta Radius Calibration (Deltabots only)
=========================================
-Define tool head characteristics and build platform diameter to get 4 generated gcode files to aid in firmware calibration


Extruder Retraction Limits
==========================
-Validate a hotend design by customizing a retraction torture test


Jerk Calibration
================
-Define machine parameters and incremental "jerk" values that will be generated into gcode.
-Watch the machine run through the generated gcode routine and take note of which jerk iteration starts to negatively affect performance.


Temperature Change
==================
-Change the temperatures(extruder, extruder 1st layer, build platform, build platform 1st layer) of pre-existing gcode files without needing a re-slice.
-All motion commands will be preserved, allowing for objective temp quality comparisons, or identical prints with different materials or brands of plastic.
