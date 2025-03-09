import xalglib

from abaqus import *
from abaqusConstants import *
import __main__
from odbAccess import *
from sys import argv,exit
import visualization
import assembly

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior



def	dataT ():
	odbName='C:\\temp\\Job-1.odb' #results path
	odb = session.openOdb(name=odbName)
	session.viewports['Viewport: 1'].setValues(displayedObject=odb) 

	vps = session.viewports[session.currentViewportName]
	#odbName = vps.displayedObject.name
	currentstepnumber = vps.odbDisplay.fieldFrame[0]
	currentstepname = session.odbs[odbName].steps.keys()[currentstepnumber]
	currentframe = vps.odbDisplay.fieldFrame[1]
	currentsteptime = session.odbs[odbName].steps[currentstepname].frames[currentframe].frameValue

	assembly = odb.rootAssembly
	instanceList = assembly.instances.keys()
	instanceName=instanceList[0]
	
	node=473		#node number
	node=node-1
	thePointList= []
	TemperatureList=[]
	
	#Coordinates from node
	coordsX=assembly.instances[instanceName].nodes[node].coordinates[0]
	coordsY=assembly.instances[instanceName].nodes[node].coordinates[1] 
	coordsZ=assembly.instances[instanceName].nodes[node].coordinates[2]
	coords = (coordsX, coordsY, coordsZ)
	thePointList.extend([coords])

	for x in range (1, currentframe+1):
		TemperaturaXYData=session.XYDataFromPath(name='Temperatura',path=session.Path(name='track', type=POINT_LIST, expression=thePointList), 
			includeIntersections=False, shape=UNDEFORMED, labelType=TRUE_DISTANCE, step=0, frame=x,  variable=(('NT11', NODAL),))
		
		Temperature = TemperaturaXYData.data[0]
		TemperatureList.extend([Temperature[1]])
		
	odb.close
	return TemperatureList
        

Mdb()
openMdb(pathName='C:\\temp\\figura.cae')
def gr2_z1(alpha):
    print(alpha)
    mdb.models['Model-1'].interactionProperties['IntProp-1'].setValues(
        temperatureDependency=OFF, dependencies=0, property=((alpha/1000, ), ))
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
    mdb.jobs['Job-1'].waitForCompletion()


	
def function1(p, fi, param):
    f0 = [200,144.8127899,97.45737457,67.24383545,48.55483246,37.16452026,30.28382683]
    fi[0] = 0
    gr2_z1(p[0])

    wyniki = dataT()
    print("alpha")
    print(p[0])
    print("wyniki")
    print(wyniki)
    for i in range(6):
        fi[0] = fi[0] + (wyniki[i] - f0[i])**2
    print("funkcja celu po optymalizacji")
    print(fi[0])

    print(p)
    global m
    print("iteration: ", m)
    print("fi: ", fi[0])
    m = m + 1
    return

p = [0.4]				#definicja poczatkowych wartosci wektora rozwiazan
bndl = [0.4]			#ograniczenia dolne
bndu = [1.0]			#ograniczenia gorne
epsx = 0.01		        #kryterium stopu
maxits = 0  			#Maksymalna liczba iteracji, jezeli maxits=0 to liczba iteracji jest nieograniczona
m = 1					#liczba funkcji celu
DiffStep = 0.0001		#numeryczny krok rozniczkowania

state = xalglib.minlmcreatev(m, p, DiffStep)
xalglib.minlmsetbc(state, bndl, bndu)
xalglib.minlmsetcond(state, epsx, maxits)
xalglib.minlmoptimize_v(state, function1)
p, rep = xalglib.minlmresults(state)

print(p)

line = str(p)
Write=open(('wyniki.txt'), 'w')
Write.writelines(line)

