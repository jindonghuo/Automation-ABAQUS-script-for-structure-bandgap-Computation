# Automation by ABAQUS Python script for bandgap calculations

Hope this method can help you to use ABAQUS python script for automation. Please note Abaqus python is python 2, and the main.py is python 3 file, but they can work together very well.

## Description
This project is for large scale computing for structure optimization that can find the stuructre/geometry with best bandgap for vibration control.

## Physcial process
For spatial peroridcal structure, when subject to wave transmission/vibration, the dynamic equation(wave equation) follows Bloch's theorem. By specifying the bloch wave boundary conditions, we can do a natural freqency extraction and loop through all brillouin zone point (irreduicable brillouin zone) to get the band structure, thus to find the forbidden frequency range.
From the band structure, if there is a bandgap, the vibration frequency within that bandgap cannot propagate through the materials. This is the basic rule for accrousitc metamaterials design.

In order to find the best design of unitcell structure, the automation will loop through all possible design, do freqency calculation and serach the bandgap.

## main.py

This is the main file. And running this file will start all computation. In general, it will do the following things
* There are two geometry parameters, so two for loop will go through each parameter combinations to create the geometry.
* In order to get a good mesh, equiDistance functions will rearrange the mesh seeds points.
* Then, it will set up the simulation model for each K point (each geometry can have many wave boudnary conditions which represents difference wave length).
* Do the computaiton, and check if the result file generated, it will proceed to next job.

## setupModel.py

This is the python scripting that should by running by abaqus. This script will create a standard 2D geometry model (it is possible to extended into 3D, but need to modify all other files)
* Create the geometry using abaqus CAE command, like draw sketch
* Creat the materials and sections, and assign sections to proper geometry domain
* Setup mesh control, and element type
* Make instanace in assembly
* Copy the part 1 and translate to another location and rename to part 2, becasue the bloch wave boudary conditions using complex number, which cannot be realized in ABAUQS, but we overcome this by create two part (key point, but a little difficult to understand).
* Specify the fieldoutput, which is just used to see the vibration modes.
* The eigenvalue/frequency is stored in *.dat file

## PBCSetup.py

This is the key file for setting up the wave boundary conditions. From this file, you can see 
* How to use node coordinates to search note and create note set 
* How to setup equation constrints in ABAQUS, which is very flexible and useful

## readEigenvalue.py

This file is for postprocess, which parses the *.dat file for the natural frequency value.
* extract all natural frequency data for each geometry configurations.
* serach the bandgap
* write the bandgap for every geometry parameter pairs.

## Below is the design geometry parameter space
![alt text](https://github.com/jindonghuo/Automation-ABAQUS-script-for-bandgap-calculation/blob/68540c3690d9b7b54330c13bf3768a0b2fe6aaf7/geometry%20space.png)

## Authors
Jindong Huo
