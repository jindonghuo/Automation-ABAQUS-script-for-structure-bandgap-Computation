#! /user/bin/python
#- * -coding: UTF-8- * -
# -*- coding: mbcs -*-tes
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqus import *
from abaqusConstants import *
from odbAccess import *

import sys
import os 
import datetime
import shutil
import numpy as np

with open('XYSinCosC1C2JobID.txt', 'r') as f:
    last_line = f.readlines()[-1]
    last_line = last_line.strip('\n')
data=last_line.split() 

Xcos, Xsin, Ycos, Ysin=[float(i) for i in data[:4]]
edgeName='edge_'+data[4]+'_'+data[5]+'.txt'
jobID=int(data[6])

#execfile('KPSinCos.py')
#
modelName='Model-2D'
partName1='Part-1'
instName1='Part-1-1'
partName2='Part-2'
instName2='Part-2-1'

nEle=40
slength=29.0/2.0
MeshSize=slength/nEle

edge=[]
with open(edgeName,'r') as f: # edgeName is in  execfile('KPSinCos.py')
    for line in f:
        edge.append(list(map(float,line.split(','))))

circle=[]
with open('circle.txt','r') as f:
    for line in f:
        circle.append(list(map(float,line.split(','))))        

# Build the 2D matrix model
mdb.Model(modelType=STANDARD_EXPLICIT, name=modelName)
mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=100.0)
mdb.models[modelName].sketches['__profile__'].rectangle(point1=(-1.0*slength, -1.0*slength), 
    point2=(1.0*slength, 1.0*slength))
mdb.models[modelName].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models[modelName].parts['Part-1'].BaseShell(sketch=
    mdb.models[modelName].sketches['__profile__'])
del mdb.models[modelName].sketches['__profile__']

# Partition: draw the fractal lattice according to the edge
mdb.models[modelName].ConstrainedSketch(gridSpacing=0.14, name='__profile__', 
    sheetSize=5.65, transform=
    mdb.models[modelName].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models[modelName].parts['Part-1'].faces.findAt((-0.333333, 
    -0.333333, 0.0), (0.0, 0.0, 1.0)), sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
mdb.models[modelName].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models[modelName].sketches['__profile__'])

# Draw edge and circle
for i in range(len(edge)-1):
  x1=edge[i][0]
  y1=edge[i][1]
  x2=edge[i+1][0]
  y2=edge[i+1][1]
  mdb.models[modelName].sketches['__profile__'].Line(point1=(x1, y1), point2=(
    x2, y2))
mdb.models[modelName].sketches['__profile__'].Line(point1=(edge[-1][0], edge[-1][1]),
    point2=(edge[0][0], edge[0][1]))       # Last point

for i in range(len(circle)-1):
  x1=circle[i][0]
  y1=circle[i][1]
  x2=circle[i+1][0]
  y2=circle[i+1][1]
  mdb.models[modelName].sketches['__profile__'].Line(point1=(x1, y1), point2=(x2, y2))
mdb.models[modelName].sketches['__profile__'].Line(point1=(circle[-1][0], circle[-1][1]),
    point2=(circle[0][0], circle[0][1]))             # add the last point

mdb.models[modelName].parts['Part-1'].PartitionFaceBySketch(faces=
    mdb.models[modelName].parts['Part-1'].faces.findAt(((-0.333333, -0.333333, 
    0.0), )), sketch=mdb.models[modelName].sketches['__profile__'])
del mdb.models[modelName].sketches['__profile__'] 

# materials and sections
mdb.models[modelName].Material(name='Foam')
mdb.models[modelName].materials['Foam'].Density(table=((0.115e-09, ), ))
mdb.models[modelName].materials['Foam'].Elastic(table=((8.0, 0.33), ))
mdb.models[modelName].Material(name='Rubber')
mdb.models[modelName].materials['Rubber'].Density(table=((1.3e-09, ), ))
mdb.models[modelName].materials['Rubber'].Elastic(table=((11.75e-2, 0.469), ))
mdb.models[modelName].Material(name='Lead')
mdb.models[modelName].materials['Lead'].Density(table=((11.6e-09, ), ))
mdb.models[modelName].materials['Lead'].Elastic(table=((40800, 0.37), ))

mdb.models[modelName].HomogeneousSolidSection(material='Foam', name='Foam', thickness=1.0)
mdb.models[modelName].HomogeneousSolidSection(material='Rubber', name='Rubber', thickness=1.0)
mdb.models[modelName].HomogeneousSolidSection(material='Lead', name='Lead', thickness=1.0)

#
mdb.models[modelName].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models[modelName].parts['Part-1'].faces.findAt(((0.0, 
    0.0, 0.0), ), )), sectionName='Lead', thicknessAssignment=FROM_SECTION)
mdb.models[modelName].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models[modelName].parts['Part-1'].faces.findAt(((edge[3][0]-0.02, edge[3][1], 
    0.0), ), )), sectionName='Rubber', thicknessAssignment=FROM_SECTION)   
mdb.models[modelName].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models[modelName].parts['Part-1'].faces.findAt(((-1.0*slength, -1.0*slength, 
    0.0), ), )), sectionName='Foam', thicknessAssignment=FROM_SECTION)
#Set the element type

# Mesh control
mdb.models[modelName].parts['Part-1'].setMeshControls(elemShape=QUAD_DOMINATED, regions=
    mdb.models[modelName].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), )))
mdb.models[modelName].parts['Part-1'].setMeshControls(elemShape=QUAD_DOMINATED, regions=
    mdb.models[modelName].parts['Part-1'].faces.findAt(((edge[0][0]-0.1, edge[0][1], 0.0), )))    
mdb.models[modelName].parts['Part-1'].setMeshControls(elemShape=QUAD_DOMINATED, regions=
    mdb.models[modelName].parts['Part-1'].faces.findAt(((-1.0*slength, -1.0*slength, 0.0), )))

# Element Type
mdb.models[modelName].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT),
    ElemType(elemCode=CPE3, elemLibrary=STANDARD)), regions=(
    mdb.models[modelName].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), )), ))
mdb.models[modelName].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT),
    ElemType(elemCode=CPE3, elemLibrary=STANDARD)), regions=(
    mdb.models[modelName].parts['Part-1'].faces.findAt(((edge[3][0]-0.02, edge[3][1], 0.0), )), ))
mdb.models[modelName].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT),
    ElemType(elemCode=CPE3, elemLibrary=STANDARD)), regions=(
    mdb.models[modelName].parts['Part-1'].faces.findAt(((-1.0*slength, -1.0*slength, 0.0), )), ))


'''
mdb.models['Model-2D'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE8, elemLibrary=STANDARD), ElemType(elemCode=CPE6, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-2D'].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), )), ))
mdb.models['Model-2D'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE8, elemLibrary=STANDARD), ElemType(elemCode=CPE6, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-2D'].parts['Part-1'].faces.findAt(((edge[3][0]-0.02, edge[3][1], 0.0), )), ))
mdb.models['Model-2D'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE8, elemLibrary=STANDARD), ElemType(elemCode=CPE6, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-2D'].parts['Part-1'].faces.findAt(((-1.0*slength, -1.0*slength, 0.0), )), ))
'''


# Seeds and Mesh
mdb.models[modelName].parts['Part-1'].seedPart(deviationFactor=0.1, minSizeFactor=0.05, size=MeshSize)
mdb.models[modelName].parts['Part-1'].generateMesh()

# Copy and Assembly
mdb.models[modelName].Part(name='Part-2', objectToCopy=mdb.models[modelName].parts['Part-1'])
mdb.models[modelName].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models[modelName].rootAssembly.Instance(dependent=ON, name=instName1, 
    part=mdb.models[modelName].parts['Part-1'])
mdb.models[modelName].rootAssembly.Instance(dependent=ON, name=instName2, 
    part=mdb.models[modelName].parts['Part-2'])

# move the partName2
mdb.models[modelName].rootAssembly.translate(instanceList=(instName2, ), vector=(60.0, 0.0, 0.0))

# PBC
execfile('PBCSetup.py')

# Step and Output
mdb.models[modelName].FrequencyStep(name='Step-1', numEigen=80, previous='Initial')
mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'MISES', 'MISESMAX', 'CTSHR', 'ALPHA', 'MISESONLY', 'PRESSONLY', 'E', 
    'EE', 'IE', 'NE', 'LE', 'ER', 'U'))

jobName='Job-'+str(jobID)
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=modelName, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=jobName, nodalOutputPrecision=FULL, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, 
    userSubroutine='', waitHours=0, waitMinutes=0)

mdb.jobs[jobName].writeInput()
#mdb.jobs[jobName].submit(consistencyChecking=OFF)
sys.exit()