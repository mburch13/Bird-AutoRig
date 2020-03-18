#create mesh

import maya.cmds as cmds
global size
global name

def returnName():
	return cmds.textFieldGrp(name, q = True, text = True)
		
def returnSize():
	return cmds.intSliderGrp(size, q = True, value = True)

def createMeshes(objName, objSize):
	global size
	global name
	size = objSize
	name = objName
	size = returnSize()
	name = returnName()
	
	cmds.polyCube(h = size, sy = size)
	cmds.rename(name)
	cmds.move(0, size/2.0, 0)
	
	cmds.makeIdentity(apply=True, t=1, s=1)