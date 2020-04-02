import maya.cmds as cmds
import birdLoc as loc
import birdJoints as jnts
import birdAnim as anim

loc = reload(loc)
jnts = reload(jnts)
anim = reload(anim)

class Rig():
    def __init__(self):
    	self.BuildUI()
	
    def BuildUI(self):
        cmds.window("Bird Rig")
        cmds.rowColumnLayout(nc = 1, adjustableColumn = True)

        cmds.button('Create Locators', w=200, c='loc.locators()')
        cmds.button('Create Rig', w=200, c='jnts.createRig()')
        cmds.button('Bind Skin', w=200, c='jnts.BindSkin()')
        cmds.button('Animate Character', w=200, c='anim.birdAnim()')
        cmds.button('Clear', w=200, c=self.clearScene)
        cmds.showWindow()
        
    def clearScene(self, void):
		cmds.delete('Joints')
		cmds.delete('ctrl*')
		print 'Scene Clearded'
		
Rig()