#create bird locators

import maya.cmds as cmds

def locators():
    #root locator
    root = cmds.spaceLocator(n='loc_root')
    cmds.move(0,3,0)
    cmds.scale(.5,.5,.5)

    #hip connection for the legs
    hipCon = cmds.spaceLocator(n='loc_spine_hip_connect')
    cmds.move(0,1.5,-.5)
    cmds.scale(.5,.5,.5)
    cmds.parent(hipCon, root)

    #spine locator
    body = cmds.spaceLocator(n='loc_spine_body')
    cmds.move(0,2,0)
    cmds.scale(.5,.5,.5)
    cmds.parent(body, root)

    #create and group the left wing locators
    locGrp = cmds.group(n='Locators_Left_Wing', em=True)
    cmds.parent(locGrp, root)
    shoulder = cmds.spaceLocator(n='loc_wing_shoulder')
    cmds.move(.7, 3.1, 0.05)
    cmds.scale(.2,.2,.2)
    cmds.parent(shoulder, locGrp)

    elbow=cmds.spaceLocator(n='loc_wing_elbow')
    cmds.move(1.4, 1.7, -.7)
    cmds.scale(.2,.2,.2)
    cmds.parent(elbow, locGrp)

    mid=cmds.spaceLocator(n='loc_wing_mid')
    cmds.move(2.2, 3.5, .46)
    cmds.scale(.2,.2,.2)
    cmds.parent(mid, locGrp)

    tip=cmds.spaceLocator(n='loc_wing_tip')
    cmds.move(4.6, 2.6, 0)
    cmds.parent(tip, locGrp)

    #duplicate and rename left wing locators for the right side
    cmds.select(locGrp)
    cmds.duplicate(n='Locators_Right_Wing',rr=True, rc=False)
    cmds.scale(-2,2,2)

    #create and group left leg locators
    locGrp2 = cmds.group(n='Locators_Left_Leg', em=True)
    cmds.parent(locGrp2, root)
    leg = cmds.spaceLocator(n='loc_leg')
    cmds.move(.42,1.15,-.35)
    cmds.scale(.5,.5,.5)
    cmds.parent(leg, locGrp2)

    knee = cmds.spaceLocator(n='loc_leg_knee')
    cmds.move(.5,.57,-.15)
    cmds.scale(.5,.5,.5)
    cmds.parent(knee, locGrp2)

    ankle = cmds.spaceLocator(n='loc_leg_ankle')
    cmds.move(.5,.16,.12)
    cmds.scale(.5,.5,.5)
    cmds.parent(ankle, locGrp2)

    #duplicate and rename left leg locators for the right side
    cmds.select(locGrp2)
    cmds.duplicate(n='Locators_Right_Leg',rr=True, rc=True)
    cmds.scale(-2,2,2)
    print 'locators created'
