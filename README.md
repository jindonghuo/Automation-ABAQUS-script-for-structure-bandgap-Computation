# Automation by ABAQUS + Python script for phononic bandgap computation


## Contributor
Jindong Huo

## Description
Througth topology/geometry optimization, this project aims to find the target structure/geometry configuration with the best bandgap for the control of wave transmission.
This method takes advantage of ABAQUS + python script for automation. Please note Abaqus python is python 2, and the main.py is python 3, but they can work together very well.

## Physcial process
For spatial peroridcal structure, when subject to wave transmission, the dynamic equation(wave equation) follows Bloch's theorem. By specifying the bloch wave boundary conditions, we can do a natural freqency extraction and loop through all Brillouin zone points (irreduicable brillouin zone) to calculate the dispersion relation, namely the band structure, to find the forbidden frequency range or bandgap.
If there is a gap in the calcuated band structure, the wave that its frequency is within that bandgap cannot propagate through the meta-materials. This is the basic rule for accrousitc metamaterials design.

In order to find the best design of unitcell structure, the automation will loop through all possible design, do freqency calculation and serach the bandgap. In other words this is a brute force search. So please refer to below paper for the efficient DGD algorith for searching: 
https://iopscience.iop.org/article/10.1088/1361-665X/acc36c/meta

## main.py

Running this file will start the entire automation flow. In general, it will do the following things
* There are two shape feature parameters (or choose more shape features), so two nested for loop will go through each parameter pair to create the geometry.
* In order to get a good mesh, equiDistance functions will rearrange the mesh seeds points based-on equal-distance (instead of equal angle in polo-coordinate).
* Then, it will set up the simulation model for each K point (the point in 1st Brillouin zone boundary. Different K values represent difference wave lengths).
* Do the computaiton, and check if the result  generated, and then it will proceed to next job.

## setupModel.py

This is the python scripting that should be executed by abaqus kernal. This script will create a standard 2D geometry model (it can be extended into 3D, but need to modify other files)
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

## Below is the design space of geometry parameters
![alt text](https://github.com/jindonghuo/Automation-ABAQUS-script-for-bandgap-calculation/blob/68540c3690d9b7b54330c13bf3768a0b2fe6aaf7/geometry%20space.png)

