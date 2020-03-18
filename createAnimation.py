#create animation
import maya.cmds as cmds

def createAnimation():
	
	freq = .1
	offset = 0
	amp = 10

	cmds.expression(s = 'ctrl_0.rotateZ = sin((frame*.1)+0)*10')

	cmds.expression(s = 'ctrl_2.rotateZ = sin((frame*.1)+0)*10')
