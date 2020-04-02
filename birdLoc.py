#bird locators

import maya.cmds as cmds

def locators():
    root = cmds.spaceLocator(n='loc_root')
    cmds.move(0,1.5,-.5)
    cmds.scale(.5,.5,.5)

    body = cmds.spaceLocator(n='loc_spine_body')
    cmds.move(0,2,0)
    cmds.scale(.5,.5,.5)
    cmds.parent(body, root)
    
    wingCon = cmds.spaceLocator(n='loc_spine_wing_connect')
    cmds.move(0,3,0)
    cmds.scale(.5,.5,.5)
    cmds.parent(wingCon, root)
    
    locGrp = cmds.group(n='Locators_Left_Wing', em=True)
    cmds.parent(locGrp, root)
    for i in range(6):
        l = cmds.spaceLocator(n='loc_wing_'+str(i+1))
        cmds.move(.4+(i/3.0), 3+(i/9.0), i/10.0)
        cmds.scale(.2,.2,.2)
        cmds.parent(l, locGrp)
    tip=cmds.spaceLocator(n='loc_wing_tip')
    cmds.move(4.6, 2.6, 0)
    cmds.parent(tip, locGrp)    
    
    cmds.select(locGrp)
    cmds.duplicate(n='Locators_Right_Wing',rr=True, rc=False)
    cmds.scale(-2,2,2)
    
    
    
    
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
    
    cmds.select(locGrp2)
    cmds.duplicate(n='Locators_Right_Leg',rr=True, rc=True)
    cmds.scale(-2,2,2)
    print 'locators created'
    