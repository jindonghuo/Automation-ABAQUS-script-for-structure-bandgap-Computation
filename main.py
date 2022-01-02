import subprocess
import sys
import os, glob
import time
import datetime
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# created by Jindong Huo, huojindong@gamil.com
def equiDistance(x, y, dL):
    Darray=np.sqrt((x[1:]-x[:-1])**2+(y[1:]-y[:-1])**2)
    Dcum=[np.sum(Darray[:i+1]) for i in range(len(Darray))]
    xf=np.array([x[0]])
    yf=np.array([y[0]])
    NN=1
    for i, CL in enumerate(Dcum):
        if CL<NN*dL: continue
        while CL>=NN*dL:
            Dd1=CL-NN*dL
            Dd=Darray[i]
            xnew=x[i]+(x[i+1]-x[i])*(Dd-Dd1)/Dd
            ynew=y[i]+(y[i+1]-y[i])*(Dd-Dd1)/Dd
            xf=np.append(xf, xnew)
            yf=np.append(yf, ynew)
            NN+=1   
    return xf, yf
#
def writeSbatchFile(sbatchfilename, py_code1, count):    
    partitions = ['SkylakePriority','debug','general','HaswellPriority','serial','general_requeue','parallel']
    fb=open(sbatchfilename,'w')
    fb.write('#!/bin/bash \n')
    fb.write('#SBATCH --partition='+partitions[0]+'\n')
    fb.write('#SBATCH --ntasks=1  \n')
    fb.write('#SBATCH --nodes=1   \n')    
    #fb.write('#SBATCH --exclusive \n')     # to reduce abaqus interface        
    fb.write('#SBATCH --job-name=JCAE_'+str(count)+' \n')
    fb.write('#SBATCH -o output_CAE_%J.dat \n')
    fb.write('#SBATCH -e output_CAE_%J.dat \n')
    fb.write('\n')
    fb.write('\n')
    fb.write('ulimit -s unlimited \n')
    fb.write('abq2019cae cae noGUI='+py_code1+' \n')
    fb.write('exit')
    fb.close()

def writeSbatchComputation(sbatchfilename, Inpfile, count):    
    partitions = ['SkylakePriority','debug','general','HaswellPriority','serial','general_requeue','parallel']
    fb=open(sbatchfilename,'w')
    fb.write('#!/bin/bash \n')
    fb.write('#SBATCH --partition='+partitions[0]+'\n')
    fb.write('#SBATCH --ntasks=1  \n')
    fb.write('#SBATCH --nodes=1   \n')    
    #fb.write('#SBATCH --exclusive \n')     # to reduce abaqus interface        
    fb.write('#SBATCH --job-name=JINP_'+str(count)+' \n')
    fb.write('#SBATCH -o output_INP_%J.dat \n')
    fb.write('#SBATCH -e output_INP_%J.dat \n')
    fb.write('\n')
    fb.write('\n')
    fb.write('ulimit -s unlimited \n')
    fb.write('abaqus job='+Inpfile+' que=SkylakePriority:fslocal \n')
    fb.write('exit')
    fb.close()

##############################################################################################
start_time = time.time()
initdirectory = os.getcwd()
py_code1    = 'setupModel.py'
py_code2    = 'PBCSetup.py'

if not os.path.exists(os.path.join(initdirectory, py_code1)):
    print ('\n There is no ' + py_code1 + ' file in original directory, please check it.    \n')
    input('\n Press anykey to exit...')
    sys.exit()
if not os.path.exists(os.path.join(initdirectory, py_code2)):
    print ('\n There is no ' + py_code2 + ' file in original directory, please check it.    \n')
    input('\n Press anykey to exit...')
    sys.exit()

#NameSuffix = str(input('\n Please input the name suffix for job: '))
NameSuffix='Group_3'
timestr = time.strftime("%Y%m%d_%H%M%S_")
workFolder  ='D' + str(timestr) + NameSuffix
if not os.path.isdir(os.path.join(os.getcwd(), workFolder)):
    os.mkdir(workFolder)
os.chdir(os.path.join(os.getcwd(), workFolder))    # change directory to subfolder

shutil.copy(os.path.join(initdirectory, py_code1), os.getcwd())
shutil.copy(os.path.join(initdirectory, py_code2), os.getcwd())
time.sleep(0.1)               # leave some time for copy

###############################################################################################
# K point
lgpi=np.log2(np.pi)
NN=25                # 23 + 9 + 23 + 12 =67
#WNBri1=np.concatenate((np.logspace(lgpi, -2.5, NN, base=2), np.array([0.15, 0.11, 0.07, 0.03, 0, 0.03, 0.07, 0.11, 0.15]), np.logspace(-2.5, lgpi, NN, base=2), np.linspace(np.pi, np.pi, 12)), axis=0)
#WNBri2=np.concatenate((np.logspace(lgpi, -2.5, NN, base=2), np.array([0.15, 0.11, 0.07, 0.03, 0, 0, 0, 0, 0]), np.linspace(0,  0,  NN),   np.linspace(0, np.pi, 12)), axis=0)    # np.logspace(-2, logpi, num=10, endpoint=True)

WNBri1=np.concatenate((np.linspace(np.pi, 0, NN, endpoint=False), np.linspace(0, np.pi, NN, endpoint=False), np.linspace(np.pi, np.pi, NN, endpoint=False)), axis=0)
WNBri2=np.concatenate((np.linspace(np.pi, 0, NN, endpoint=False), np.linspace(0,  0,  NN, endpoint=False),   np.linspace(0, np.pi, NN, endpoint=False)), axis=0)   

fig0, ax0 = plt.subplots(figsize=(7.5, 7.5))
ax0.plot(WNBri1,  WNBri2, 'o', color='r', markersize=2, linewidth=1.0)
fig0.tight_layout()
fig0.savefig('0KPointBrillionZone.png', bbox_inches='tight',dpi=300)
plt.close()
plt.clf()

L=29
r0=5.0
phi=0.4
theta=np.linspace(0.0, 2*np.pi, num=800, endpoint=False)
dL=2*np.pi*r0/85

# inner circle only write once
x0=r0*np.cos(theta)
y0=r0*np.sin(theta)
xf0, yf0=equiDistance(x0, y0, dL)
with open('circle.txt', 'w') as f0:
    for i in range(len(xf0)):
        f0.write('{xx:.6f}, {yy:.6f} \n'.format(xx=xf0[i], yy=yf0[i]))        # write only once

###############################################################################################
#CC1= np.arange(-0.28, 0.121, step=0.04)    # -0.3, 0.15
#CC2= np.arange(-0.2, 0.201, step=0.04)     # -0.2, 0.25 
#CC1=np.array([-0.28, -0.26, -0.24,    -0.22, -0.20, -0.18,     -0.16, -0.14, -0.12,      -0.10, -0.08, -0.06,      -0.04, -0.02, 0.00,      0.02, 0.04, 0.06,      0.08, 0.10, 0.12])# 

CC1=np.array([-0.16, -0.14, -0.12])  #
CC2=np.array([-0.20, -0.18, -0.16, -0.14, -0.12, -0.10, -0.08, -0.06, -0.04, -0.02, 0.00,  0.02,  0.04,  0.06,  0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
count=0

for c1 in CC1:
    for c2 in CC2:
        R0=L*np.sqrt(2*phi)/np.sqrt(np.pi*(2+c1**2+c2**2))
        R=R0*(1+c1*np.cos(4*theta)+c2*np.cos(8*theta))

        x=R*np.cos(theta)
        y=R*np.sin(theta)
        xf, yf=equiDistance(x, y, dL)                     # treat the last item
        edgeName='edge_{:.2f}_{:.2f}.txt'.format(c1, c2)  #  +str(c1)+'_'+str(c2)+'.txt'
        with open(edgeName, 'w') as f1:
            for ii in range(len(xf)):
                f1.write('{xx:.6f}, {yy:.6f} \n'.format(xx=xf[ii], yy=yf[ii]))
        
        for k in range(len(WNBri1)):
            Xcos, Xsin=np.cos(WNBri1[k]), np.sin(WNBri1[k])
            Ycos, Ysin=np.cos(WNBri2[k]), np.sin(WNBri2[k])
            count+=1
            fcc=open('C1_C2_Counts.txt', 'a')
            fcc.write('{c11:.2f} {c22:.2f} {Countt:d} \n'.format(c11=c1, c22=c2, Countt=count))
            fcc.close()

            fk=open('XYSinCosC1C2JobID.txt', 'a')
            fk.write('{:.12f} {:.12f} {:.12f} {:.12f} {:.2f} {:.2f} {:d} \n'.format(Xcos, Xsin, Ycos, Ysin, c1, c2, count))
            fk.close()

            if sys.platform.startswith('win'):
                GUI = input('\n Would you like to run with GUI?(Y/N):  ')
                if GUI=='Y' or GUI=='y':      
                    cmd = 'abaqus cae script='+py_code1
                    print('\n '+cmd)
                else:
                    cmd = 'abaqus cae noGUI='+py_code1
                    print('\n '+cmd)
                subprocess.call(cmd)
            elif sys.platform.startswith('linux'):
                sbatchfilename = 'submit_'+str(count)+'_'+str(c1)+'_'+str(c2)+'.sh'
                writeSbatchFile(sbatchfilename, py_code1, count)
                cmd='sbatch '+sbatchfilename
                p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                out, err = p.communicate()
                out = out.decode('utf8')
                job = out.strip().split()[-1]   # this is the current jobID
                print ('\n\n  The '+sbatchfilename+' with jobID '+ str(job).strip(r'b\'')+' has been submitted. \n')
            else:
                print ('\n Unable to check the operation system, exit soon...')
                sys.exit()
            
            status=0.0
            OutputINP='Job-'+str(count)+'.inp'
            Time1=time.time()            
            while not os.path.exists(OutputINP):
                time.sleep(0.01)
                if (time.time()-Time1)>=4000: 
                    print(OutputINP+' was passed and now continue to next abaqus job \n')
                    status=1.0
                    break
            if status==1.0: continue
            ##########################################  submit the inp not in CAE
            sbatchINP = 'abqjob_'+str(count)+'.sh'
            INPFILEnoExt='Job-'+str(count)
            writeSbatchComputation(sbatchINP, INPFILEnoExt, count)  # use skylakepriority
            #time.sleep(0.01)

            cmd2='sbatch '+sbatchINP
            p = subprocess.Popen(cmd2.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # p = subprocess.Popen(cmd2.split(), stdout=subprocess.PIPE)
            out, err = p.communicate()
            out = out.decode('utf8')
            job = out.strip().split()[-1]                     # this is the current jobID
            print ('\n\n  The INP: '+sbatchINP+' with jobID '+ str(job).strip(r'b\'')+' has been submitted. \n')

time.sleep(30)                           # leave some time for last job to finish
for filename1 in glob.glob('./submit_*'):
    os.remove(filename1)    
for filename1 in glob.glob('./*.sh'):
    os.remove(filename1)    
for filename1 in glob.glob('./output_abaqus*'):
    os.remove(filename1)     
for filename1 in glob.glob('./*.log'):
    os.remove(filename1)         
for filename1 in glob.glob('./*.sta'):
    os.remove(filename1)     
for filename1 in glob.glob('./*.sim'):
    os.remove(filename1) 
for filename1 in glob.glob('./*.prt'):
    os.remove(filename1) 
for filename1 in glob.glob('./*.com'):
    os.remove(filename1) 
for filename1 in glob.glob('./*.msg'):
    os.remove(filename1)

################################################################################################################
timeseconds2 = time.time() - start_time
hour   = int(timeseconds2/3600)
minute = int((timeseconds2-hour*3600)/60)
second = int(timeseconds2-3600*hour-60*minute)
print ('\n\n Submitting '+ str(count)+ ' jobs takes {:02d}:{:02d}:{:02d} time. \n\n'.format(hour, minute, second))
sys.exit()
