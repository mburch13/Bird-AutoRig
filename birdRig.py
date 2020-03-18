import maya.cmds as cmds
import birdLoc as loc

loc = reload(loc)

class Rig():
    def __init__(self):
    	self.BuildUI()
	
    def BuildUI(self):
        cmds.window("Bird Rig")
        cmds.rowColumnLayout(nc = 1, adjustableColumn = True)

        cmds.button('Locators', w=200, c='loc.locators()')
        cmds.button('Rig', w=200, c='loc.createRig()')
        cmds.button('Bind', w=200, c='loc.BindSkin()')
        cmds.button('Clear', w=200, c=self.clearScene)
        cmds.showWindow()
        
    def clearScene(self, void):
		cmds.delete('Locators')
		cmds.delete('Joints')
		cmds.delete('Ctrl*')
		print 'Scene Clearded'
		
Rig()