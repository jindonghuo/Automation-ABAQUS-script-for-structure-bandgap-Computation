# Automation by using ABAQUS script for bandgap calculations

## Description
This project is for large scale computing for structure optimization that can find the stuructre/geometry with best bandgap for vibration control.

## Physcial process
For spatial peroridcal structure, when suject to wave transmission/vibration, the dynamic equation(wave equation) follows Bloch's theorem. By specifying the bloch wave boundary conditions, we can do a natural freqency extraction and loop through all brillouin zone (irreduicable brillouin zone) to get the band structure.
From the band structure, if there is a bandgap, the vibration frequency within that bandgap cannot propagate through the materials. This is the basic rule for accrousitc metamaterials design.

In order to find the best design of unitcell structure, the automation will loop through all possible design, do freqency calculation and serach the bandgap.

## main.py

This is the main file. And running this file will start all computation. In general, it will do the following things
* There are two geometry parameters, so two for loop will go through each parameter combinations to create the geometry.
* In order to get a good mesh, equiDistance functions will rearrange the mesh seeds points.
* Then, it will set up the simulation model for each K point (each geometry can have many wave boudnary conditions which represents difference wave length).
* Do the computaiton, and check if the result file generated, it will proceed to next job.
* 
* 

##
