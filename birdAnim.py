#create animation
import maya.cmds as cmds

def birdAnim():
	
	freq = .1
	offset = 0
	amp = 10

	cmds.expression(s = 'ctrl_2.rotateX = sin((frame*.1)+0)*10')

	cmds.expression(s = 'ctrl_9.rotateX = -sin((frame*.1)+0)*10')
