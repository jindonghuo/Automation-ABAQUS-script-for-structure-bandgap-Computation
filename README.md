# Automation by using ABAQUS script for bandgap calculations

## Description
This project is for large scale computing for structure optimization that can find the stuructre/geometry with best bandgap for vibration control.

## Physcial process
For spatial peroridcal structure, when suject to wave transmission/vibration, the dynamic equation(wave equation) follows Bloch's theorem. By specifying the bloch wave boundary conditions, we can do a natural freqency extraction and loop through all brillouin zone (irreduicable brillouin zone) to get the band structure.
From the band structure, if there is a bandgap, the vibration frequency within that bandgap cannot propagate through the materials. This is the basic rule for accrousitc metamaterials design.

In order to find the best design of unitcell structure, the automation will loop through all possible design, do freqency calculation and serach the bandgap.


## 
