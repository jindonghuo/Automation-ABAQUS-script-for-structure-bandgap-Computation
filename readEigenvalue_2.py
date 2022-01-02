#!/usr/bin/python
#!python
import os, glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def eigenfrequencyProcess(C1, C2, c1c2Counts, eignumber, datfolder):
    freqList=[]
    for case in c1c2Counts:
        if  case[0]==C1 and case[1]==C2:
            filename='Job-'+str(int(case[2]))+'.dat'
            if not os.path.exists(os.path.join(abqdatfolder, filename)): 
                print(filename+' does not exit !!!!!!!!!!!!!!!!!!!!!!!!!!\n')
                filename='Job-'+str(int(case[2])-1)+'.dat'
            if os.stat(os.path.join(abqdatfolder, filename)).st_size <= 15360: # 1*1024*1024 is 1 MB
                print(filename+' does not exit !!!!!!!!!!!!!!!!!!!!!!!!!!\n')
                filename='Job-'+str(int(case[2])-1)+'.dat'

            oepnfile=os.path.join(datfolder, filename)

            ff=open(oepnfile, 'r') 
            eiglist=[]
            while(True):
                line=ff.readline()
                line_strip = line.replace(" ","").lower()
                if ("eigenvalueoutput" in line_strip): break

            for k in range(5):
                line = ff.readline() 

            for k in range(eignumber):
                line = ff.readline()
                data = line.split()
                eiglist.append(float(data[3])) # abs(float(tmp[1]))**0.5/2./3.1415926
            freqList.append(eiglist)            
            ff.close()
    #print ("  All eigenvalues are extracted from data file \n")

    # output all the eigenvalues
    fName1='eigenvalues_C1_{a:1.2f}_C2_{b:1.2f}.txt'.format(a=C1, b=C2)
    f2= open(fName1, 'w')
    for j in freqList:
        f2.writelines(['{:.2f} '.format(kk) for kk in j])
        f2.write('\n')
    f2.close()
    #print ("      All eigenvalues are writen in eigenvalues.txt \n")

    # Plot Bandgap
    data = np.genfromtxt(fName1)
    data1 = data.T
    fig, ax = plt.subplots(figsize=(7, 5))

    for freq in data1:                           # 1st row is the 1st order eigenvalue
        ax.plot(range(1, freq.shape[0]+1), freq, linestyle='-', marker='o', color='c', markersize=3, linewidth=2)
    plt.xticks([1, 24, 47, 57])
    ax.set_xticklabels(['M','$\Gamma$','X','M'])

    # ax.legend(loc=0, fancybox=True, ncol=1, prop={'size':16})
    ax.set_ylim(0, 1500)
    ax.set_xlim(1, 57)
    plt.tight_layout()

    fName2='dispersionCurve_C1_{a:1.2f}_C2_{b:1.2f}'.format(a=C1, b=C2)
    fig.savefig(fName2+'.png', dpi=200)
    plt.close()
    #print ( "      Bandgap plotted in dierpersion-curve.png  \n")

    # Search for the band gap
    max_prev = 0
    min_prev = 0
    bandgap  = []
    for m in data1:
        max_curr = np.max(m)
        min_curr = np.min(m)
        if (min_curr > max_prev and min_curr-max_prev>3.0):
            gap = [max_prev, min_curr, 0.5*(max_prev+min_curr), min_curr-max_prev]
            bandgap.append(gap)
        max_prev = max_curr
        min_prev = min_curr

    # write bandgap
    fName3='bandgap_C1_{a:1.2f}_C2_{b:1.2f}.txt'.format(a=C1, b=C2)
    f3=open(fName3, 'w')
    for j in bandgap:
        f3.writelines(['{:.2f} '.format(kk) for kk in j])
        f3.write('\n')
    f3.close()
    print ("      Band gap position and width has been calculated. \n \n \n")
#########################################################################
# Main

folders=['A20210328_191843_Group_1', 'A20210328_192230_Group_2', 'D20210408_140839_Group_3', 'B20210331_191726_Group_4', 
        'B20210331_191809_Group_5', 'B20210331_191843_Group_6', 'C20210402_162610_Group_7']

for folder in folders:
    abqdatfolder=os.path.join(os.getcwd(), folder)
    c1c2Count=np.genfromtxt(os.path.join(abqdatfolder, 'C1_C2_Counts.txt'))
    eignum = 80

    CC1=[]
    CC2=np.array([-0.20, -0.18, -0.16, -0.14, -0.12, -0.10, -0.08, -0.06, -0.04, -0.02, 0.00,  0.02,  0.04,  0.06,  0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
    for c1c2 in c1c2Count:
        if not CC1: CC1.append(c1c2[0])
        if c1c2[0]!=CC1[-1]: CC1.append(c1c2[0])    

    #print ('This is C1 list: \n', CC1)
    #print ('This is C2 list: \n', CC2)
    
    for C1 in CC1:
        #print ('\n\n\n This is C1:', C1)
        for C2 in CC2:
            print('\n Now it is for C1={:.2f}, C2={:.2f} ! \n'.format(C1, C2))
            eigenfrequencyProcess(C1, C2, c1c2Count, eignum, abqdatfolder)