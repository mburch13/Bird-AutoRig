import maya.cmds as cmds
import createMeshes as mesh
import createRig as rig
import createAnimation as anim

mesh = reload(mesh)
rig = reload(rig)
anim = reload(anim)

global size
global name

class Rig():
	def __init__(self):
		self.BuildUI()
	
	def BuildUI(self):
		global size
		global name
		cmds.window("Mutable Rig")
		cmds.rowColumnLayout(nc = 1, adjustableColumn = True)
		
		name = cmds.textFieldGrp(l = "Object Name", text = 'objectName')
		size = cmds.intSliderGrp(l = "Object Size", min = 2, max = 10, value = 2, step = 1, field=True)
		cmds.button('Create Mesh', w = 200, c = 'mesh.createMeshes(name, size)')
		
		cmds.button('Rig Mesh', w = 200, c = 'rig.createRig(name, size)')
		cmds.button('Animate', w=200, c='anim.createAnimation()')
		
		cmds.button('Clear Scene', w=200, c=self.clearScene)
		cmds.showWindow()

	def clearScene(self, void):
		cmds.delete('obj*')
		cmds.delete('Loc*')
		cmds.delete('Jnt*')
		cmds.delete('Ctrl*')
		print 'Scene Clearded'
Rig()