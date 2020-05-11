import maya.cmds as cmds
import birdAnim as anim

anim = reload(anim)

#create GUI
class SetPose():
    def __init__(self):
    	self.BuildUI()

    def BuildUI(self):
        cmds.window("Bird Animation")
        cmds.rowColumnLayout(nc = 1, adjustableColumn = True)

        cmds.button('Up Stroke Pose', w=200, c='anim.upStroke()', ann='Pose wings as if the up stoke has been completed')
        cmds.button('Down Stroke Pose', w=200, c='anim.downStroke()', ann='Pose wings as if the down stroke has been completed')
        cmds.button('Bind Pose', w=200, c=self.reset, ann='Reset to the bind pose')
        cmds.button('Animation Wing Controls', w= 200, c='anim.userControls()',  ann='Creates animation control channels: Use only if wing channels are not present')
        cmds.button('Hover Animtion', w=200, c='anim.glideFlap()', ann='Create expressions for a hovering flight animation')
        cmds.button('Delete Animation', w=200, c=self.clearAnim, ann='Delete animation expressions')
        cmds.showWindow()

    #delete animation expressions
    def clearAnim(self, void):
        cmds.delete('CTRL_L_wing.ry', icn =True)
        cmds.delete('CTRL_R_wing.ry', icn =True)
        cmds.delete('CTRL_root.ty', icn =True)
        print 'Expressions removed'

    #reset controls to bind position
    def reset(self, void):
        cmds.setAttr('CTRL_L_leg.translate', 0,0,0)
        cmds.setAttr('CTRL_R_leg.translate', 0,0,0)
        cmds.setAttr('CTRL_root.rotate', 0,0,0)
        cmds.setAttr('CTRL_L_wing.rotate', 0,0,0)
        cmds.setAttr('CTRL_R_wing.rotate', 0,0,0)
        cmds.setAttr('CTRL_L_wing_tip.translate', 0,0,0)
        cmds.setAttr('CTRL_R_wing_tip.translate', 0,0,0)
        print 'Bind Pose'

SetPose()
