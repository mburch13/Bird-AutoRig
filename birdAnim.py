#create animation
import maya.cmds as cmds

#create extra attributes to control animation expressions
def userControls():
    cmds.select('CTRL_root')
    cmds.addAttr(ln='wingAnimation', min=0, max=1, dv=1, at='float', k=True)
    cmds.addAttr(ln='frequency', at='float', min=0, dv=1, k=True)
    cmds.addAttr(ln='averageAngle', at='float', dv=0, k=True)

    cmds.select('CTRL_R_wing')
    cmds.addAttr(ln='Wing_Control', k=True)
    cmds.addAttr(ln='frequency', at='float', min=0, dv=1, k=True)
    cmds.addAttr(ln='averageAngle', at='float', dv=0, k=True)
    cmds.addAttr(ln='strokeAmplitude', at='float', min=0, dv=90, k=True)

    cmds.select('CTRL_L_wing')
    cmds.addAttr(ln='Wing_Control', k=True)
    cmds.addAttr(ln='frequency', at='float', min=0, dv=1, k=True)
    cmds.addAttr(ln='averageAngle', at='float', dv=0, k=True)
    cmds.addAttr(ln='strokeAmplitude', at='float', min=0, dv=90, k=True)

#set the body and leg position for flying motion
def setFlying():
    cmds.setAttr('CTRL_L_leg.translate', -0.187, 0.403, -0.378)
    cmds.setAttr('CTRL_R_leg.translate', 0.17, 0.419, -0.393)
    cmds.setAttr('CTRL_root.rotateX', 43.178)

#set the pose for a completed up stroke
def upStroke():
    setFlying()
    cmds.setAttr('CTRL_R_wing.rotate', 131.363, -30.469, -27.614)
    cmds.setAttr('CTRL_L_wing.rotate', 118.575, 33.285, 14.764)

#set the pose for a completed down stroke
def downStroke():
    setFlying()
    cmds.setAttr('CTRL_R_wing.rotate', 171.959, 54.884, 76.657)
    cmds.setAttr('CTRL_L_wing.rotate', 148.804, -62.131, -72.232)

#create expressions for hovering flapping motion based on Weis-Fogh's Model for Normal Hovering
def glideFlap():
    setFlying()

    cmds.expression(n= 'rightWing', s = 'float $pi = 3.14; \nCTRL_R_wing.rotateY = ((CTRL_root.averageAngle + CTRL_R_wing.averageAngle) + (.5 * CTRL_R_wing.strokeAmplitude * sin(2 * $pi * CTRL_R_wing.frequency * time))) * CTRL_root.wingAnimation')
    cmds.expression(n= 'leftWing', s = 'float $pi = 3.14; \nCTRL_L_wing.rotateY = ((CTRL_root.averageAngle + CTRL_L_wing.averageAngle) - (.5 * CTRL_L_wing.strokeAmplitude * sin(2 * $pi * CTRL_L_wing.frequency * time))) * CTRL_root.wingAnimation')
    cmds.expression(n='bodyPulse', s = 'float $amp = 1; \nfloat $pos = 1; \nfloat $pi = 3.14; \nCTRL_root.translateY = ($pos + (.5 * $amp * sin(2 * $pi * CTRL_root.frequency * time))) * CTRL_root.wingAnimation')
