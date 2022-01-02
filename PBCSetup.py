# create the vertices, and edges for the part1  
def Get_Cube_dimension(modelName,instanceName):    
    node=mdb.models[modelName].rootAssembly.instances[instanceName].nodes
    Xmin, Xmax=node[0].coordinates[0], node[0].coordinates[0]
    Ymin, Ymax=node[0].coordinates[1], node[0].coordinates[1]  # use any point in the nodes set, do not use 0
    for i in range(len(node)):
        x=node[i].coordinates[0]
        y=node[i].coordinates[1]
        if(Xmin>x):
            Xmin=x
        elif(Xmax<x):
            Xmax=x
        if(Ymin>y):
            Ymin=y
        elif(Ymax<y):
            Ymax=y
    return(Xmin,Xmax,Ymin,Ymax)

def MeshHandlingCube1(modelName,instanceName,Dimension):
    Xmin, Xmax=Dimension[0], Dimension[1]
    Ymin, Ymax=Dimension[2], Dimension[3]
    eps1=abs(Xmax-Xmin)*0.0001
    eps2=abs(Xmax-Xmin)*0.001
    BX, BY=Xmax-Xmin, Ymax-Ymin

    node=mdb.models[modelName].rootAssembly.instances[instanceName].nodes
    node_E1=node[1:1]
    node_E2=node[1:1]
    node_E3=node[1:1]
    node_E4=node[1:1]
    
    for i in range(len(node)):
        x=node[i].coordinates[0]
        y=node[i].coordinates[1]
        if((abs(x-Xmin)<eps1)and(abs(y-Ymin)<eps1)):
            node_v1=node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymin)<eps1)):
            node_v2=node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymax)<eps1)):
            node_v3=node[i:i+1]
        elif((abs(x-Xmin)<eps1)and(abs(y-Ymax)<eps1)):
            node_v4=node[i:i+1]
    # edge doesn't include verticles
        elif((abs(x-Xmin)<eps1)and(abs(y-Ymin)>eps2)and(abs(y-Ymax)>eps2)):
            node_E1=node_E1+node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymin)>eps2)and(abs(y-Ymax)>eps2)):
            node_E2=node_E2+node[i:i+1]
        elif((abs(y-Ymin)<eps1)and(abs(x-Xmin)>eps2)and(abs(x-Xmax)>eps2)):
            node_E3=node_E3+node[i:i+1]
        elif((abs(y-Ymax)<eps1)and(abs(x-Xmin)>eps2)and(abs(x-Xmax)>eps2)):
            node_E4=node_E4+node[i:i+1]
#    
    mdb.models[modelName].rootAssembly.Set(name='Vertice 1_R', nodes=node_v1)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 2_R', nodes=node_v2)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 3_R', nodes=node_v3)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 4_R', nodes=node_v4)
    mdb.models[modelName].rootAssembly.Set(name='edge1 I_R',   nodes=node_E1)
    mdb.models[modelName].rootAssembly.Set(name='edge2 II_R',  nodes=node_E2)
    mdb.models[modelName].rootAssembly.Set(name='edge3 III_R', nodes=node_E3)
    mdb.models[modelName].rootAssembly.Set(name='edge4 IV_R',  nodes=node_E4)
    print  'E1',len(node_E1),len(node_E2),len(node_E3),len(node_E4)

    # Edges I and II 
    countII = 0
    for i, n1 in enumerate(node_E1):
        x_1 = n1.coordinates[0]
        y_1 = n1.coordinates[1]
        nodeLabel = 'Node_I_R_'+str(i)
        mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E1[(i):(i+1)])    
        for j, n2 in enumerate(node_E2):
            x_2 = n2.coordinates[0]
            y_2 = n2.coordinates[1]
            distance=abs((x_1-x_2)**2+(y_1-y_2)**2-(BX)**2)
            if (distance<=1e-5):
                countII += 1    
                nodeLabel = 'Node_II_R_'+str(i)
                mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E2[(j):(j+1)])
                used = j
                break                    
        node_E2 = node_E2[:used] + node_E2[(used+1):]        
    if (countII!=len(node_E1)): print "Node matching edge I-II has failed"
                
    # Edges III and IV
    countIV = 0
    for i, n1 in enumerate(node_E3):
        x_1 = n1.coordinates[0]
        y_1 = n1.coordinates[1]
        nodeLabel = 'Node_III_R_'+str(i)
        mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E3[(i):(i+1)])    
        for j, n2 in enumerate(node_E4):
            x_2 = n2.coordinates[0]
            y_2 = n2.coordinates[1]
            distance=abs((x_1-x_2)**2+(y_1-y_2)**2-(BY)**2)
            if (distance<=1e-5):
                countIV = countIV + 1
                nodeLabel = 'Node_IV_R_'+str(i)
                mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E4[(j):(j+1)])
                used = j
                break                    
        node_E4 = node_E4[:used] + node_E4[(used+1):]        
    if (countIV!=len(node_E3)): print "Node matching edge III-IV has failed"
    print 'Creat Mesh sets in Part1 Complete'     

def MeshHandlingCube2(modelName,instanceName,Dimension):
    Xmin, Xmax=Dimension[0], Dimension[1]
    Ymin, Ymax=Dimension[2], Dimension[3]
    eps1=abs(Xmax-Xmin)*0.0001
    eps2=abs(Xmax-Xmin)*0.001
    BX=Xmax-Xmin;BY=Ymax-Ymin

    node=mdb.models[modelName].rootAssembly.instances[instanceName].nodes
    node_E1=node[1:1]
    node_E2=node[1:1]
    node_E3=node[1:1]
    node_E4=node[1:1]
    
    for i in range(len(node)):
        x=node[i].coordinates[0]
        y=node[i].coordinates[1]
        if((abs(x-Xmin)<eps1)and(abs(y-Ymin)<eps1)):
            node_v1=node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymin)<eps1)):
            node_v2=node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymax)<eps1)):
            node_v3=node[i:i+1]
        elif((abs(x-Xmin)<eps1)and(abs(y-Ymax)<eps1)):
            node_v4=node[i:i+1]
        #  edge doesn't include vertices
        elif((abs(x-Xmin)<eps1)and(abs(y-Ymin)>eps2)and(abs(y-Ymax)>eps2)):
            node_E1=node_E1+node[i:i+1]
        elif((abs(x-Xmax)<eps1)and(abs(y-Ymin)>eps2)and(abs(y-Ymax)>eps2)):
            node_E2=node_E2+node[i:i+1]
        elif((abs(y-Ymin)<eps1)and(abs(x-Xmin)>eps2)and(abs(x-Xmax)>eps2)):
            node_E3=node_E3+node[i:i+1]
        elif((abs(y-Ymax)<eps1)and(abs(x-Xmin)>eps2)and(abs(x-Xmax)>eps2)):
            node_E4=node_E4+node[i:i+1]
    #
    mdb.models[modelName].rootAssembly.Set(name='Vertice 1_I', nodes=node_v1)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 2_I', nodes=node_v2)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 3_I', nodes=node_v3)
    mdb.models[modelName].rootAssembly.Set(name='Vertice 4_I', nodes=node_v4)
    mdb.models[modelName].rootAssembly.Set(name='edge1 I_I',   nodes=node_E1)
    mdb.models[modelName].rootAssembly.Set(name='edge2 II_I',  nodes=node_E2)
    mdb.models[modelName].rootAssembly.Set(name='edge3 III_I', nodes=node_E3)
    mdb.models[modelName].rootAssembly.Set(name='edge4 IV_I',  nodes=node_E4)
    print  'E1',len(node_E1),len(node_E2),len(node_E3),len(node_E4)

    # Edges I and II
    countII = 0
    for i, n1 in enumerate(node_E1):
        x_1 = n1.coordinates[0]
        y_1 = n1.coordinates[1]
        nodeLabel = 'Node_I_I_'+str(i)
        mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E1[(i):(i+1)])    
        for j, n2 in enumerate(node_E2):
            x_2 = n2.coordinates[0]
            y_2 = n2.coordinates[1]
            distance=abs((x_1-x_2)**2+(y_1-y_2)**2-(BX)**2)
            if (distance<=1e-5):
                countII += 1    
                nodeLabel = 'Node_II_I_'+str(i)
                mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E2[(j):(j+1)])
                used = j
                break                    
        node_E2 = node_E2[:used] + node_E2[(used+1):]        
    if (countII!=len(node_E1)): print "Node matching edge I-II has failed"
                
    # Edges III and IV 
    countIV = 0
    for i, n1 in enumerate(node_E3):
        x_1 = n1.coordinates[0]
        y_1 = n1.coordinates[1]
        nodeLabel = 'Node_III_I_'+str(i)
        mdb.models[modelName].rootAssembly.Set(name=nodeLabel,nodes=node_E3[(i):(i+1)])    
        for j, n2 in enumerate(node_E4):
            x_2 = n2.coordinates[0]
            y_2 = n2.coordinates[1]
            distance=abs((x_1-x_2)**2+(y_1-y_2)**2-(BY)**2)
            if (distance<=1e-5):
                countIV += 1    
                nodeLabel = 'Node_IV_I_'+str(i)
                mdb.models[modelName].rootAssembly.Set(name=nodeLabel, nodes=node_E4[(j):(j+1)])
                used = j
                break                    
        node_E4 = node_E4[:used] + node_E4[(used+1):]        
    if (countIV!=len(node_E3)): print "Node matching edge III-IV has failed"
    print 'Creat Mesh sets in Part2 Complete'     

def defPbcEquationConstraint(modelName):
    # Verticle                  4  3
    # The 'u' equation          1  2
    mdb.models[modelName].Equation(name='3-4 Vertice on u-R',
        terms=((-1.0,'Vertice 3_R', 1), (Xcos, 'Vertice 4_R', 1), (-Xsin, 'Vertice 4_I', 1)))
    mdb.models[modelName].Equation(name='3-4 Vertice on u-I',
        terms=((-1.0,'Vertice 3_I', 1), (Xsin, 'Vertice 4_R', 1), (Xcos, 'Vertice 4_I', 1)))
    # The 'v' equation
    mdb.models[modelName].Equation(name='3-4 Vertice on v-R',
        terms=((-1.0,'Vertice 3_R', 2), (Xcos, 'Vertice 4_R', 2), (-Xsin, 'Vertice 4_I', 2)))
    mdb.models[modelName].Equation(name='3-4 Vertice on v-I',
        terms=((-1.0,'Vertice 3_I', 2), (Xsin, 'Vertice 4_R', 2), (Xcos, 'Vertice 4_I', 2)))
    
    # The 'u' equation
    mdb.models[modelName].Equation( name='2-1 Vertice on u-R',
        terms=((-1.0,'Vertice 2_R', 1), (Xcos, 'Vertice 1_R', 1), (-Xsin, 'Vertice 1_I', 1)))
    mdb.models[modelName].Equation( name='2-1 Vertice on u-I',
        terms=((-1.0,'Vertice 2_I', 1), (Xsin, 'Vertice 1_R', 1), (Xcos, 'Vertice 1_I', 1)))
    # The 'v' equation 
    mdb.models[modelName].Equation( name='2-1 Vertice on v-R',
        terms=((-1.0,'Vertice 2_R', 2), (Xcos, 'Vertice 1_R', 2), (-Xsin, 'Vertice 1_I', 2)))
    mdb.models[modelName].Equation( name='2-1 Vertice on v-I',
        terms=((-1.0,'Vertice 2_I', 2), (Xsin, 'Vertice 1_R', 2), (Xcos, 'Vertice 1_I', 2)))
    
    # edges I-II
    maxIndex = len(mdb.models[modelName].rootAssembly.sets['edge1 I_R'].nodes)
    for i in range(maxIndex):    
        N_I_R  = 'Node_I_R_' +str(i)
        N_II_R = 'Node_II_R_'+str(i)
        N_I_I  = 'Node_I_I_' +str(i)
        N_II_I = 'Node_II_I_'+str(i)
        # The 'U' equation 
        eqName = 'Edge_II_I_' + str(i) + ' on u-R'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_II_R, 1), (Xcos, N_I_R, 1), (-Xsin, N_I_I, 1)))
        eqName = 'Edge_II_I_' + str(i) + ' on u-I'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_II_I, 1), (Xsin, N_I_R, 1), (Xcos, N_I_I, 1)))
        # The 'V' equation 
        eqName = 'Edge_II_I_' + str(i) + ' on v-R'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_II_R, 2), (Xcos, N_I_R, 2), (-Xsin, N_I_I, 2)))
        eqName = 'Edge_II_I_' + str(i) + ' on v-I'
        mdb.models[modelName].Equation( name=eqName,
            terms=((-1.0, N_II_I, 2), (Xsin, N_I_R, 2), (Xcos, N_I_I, 2)))

    # edge III-IV
    maxIndex = len(mdb.models[modelName].rootAssembly.sets['edge3 III_I'].nodes)
    for i in range(maxIndex):    
        N_IV_R  = 'Node_IV_R_' + str(i)
        N_III_R = 'Node_III_R_'+ str(i)
        N_IV_I  = 'Node_IV_I_' + str(i)
        N_III_I = 'Node_III_I_'+ str(i)
        # The 'u' equation (Abaqus coordinate 1)
        eqName = 'Edge_III_IV_' + str(i) + ' on u-R'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_IV_R, 1), (Ycos, N_III_R, 1), (-Ysin, N_III_I, 1)))
        eqName = 'Edge_III_IV_' + str(i) + ' on u-I'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_IV_I, 1), (Ysin, N_III_R, 1), (Ycos, N_III_I, 1)))
        # The 'v' equation (Abaqus coordinate 2)
        eqName = 'Edge_III_IV_' + str(i) + ' on v-R'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_IV_R, 2), (Ycos, N_III_R, 2), (-Ysin, N_III_I, 2)))
        eqName = 'Edge_III_IV_' + str(i) + ' on v-I'
        mdb.models[modelName].Equation(name=eqName,
            terms=((-1.0, N_IV_I, 2), (Ysin, N_III_R, 2), (Ycos, N_III_I, 2)))
    print 'Define BC Complete'
    
# Main
Dimension1=Get_Cube_dimension(modelName, instName1)
print 'In part1, Xmin,Xmax,Ymin,Ymax=',Dimension1
MeshHandlingCube1(modelName,instName1, Dimension1)
#
Dimension2=Get_Cube_dimension(modelName,instName2)
print 'In part2, Xmin, Xmax, Ymin, Ymax=', Dimension2
MeshHandlingCube2(modelName,instName2,Dimension2)
#
defPbcEquationConstraint(modelName)