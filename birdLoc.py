#bird locators

import maya.cmds as cmds

def locators():
    locGrp = cmds.group(n='Locators_Left', em=True)
    root = cmds.spaceLocator(n='loc_0')
    cmds.move(0,3,0)
    cmds.scale(.5,.5,.5)
    cmds.parent(locGrp, root)
    for i in range(6):
        l = cmds.spaceLocator(n='loc_'+str(i+1))
        cmds.move(.4+(i/3.0), 3+(i/9.0), i/10.0)
        cmds.scale(.2,.2,.2)
        cmds.parent(l, locGrp)
    tip=cmds.spaceLocator(n='loc_7')
    cmds.move(4.6, 2.6, 0)
    cmds.parent(tip, locGrp)
    cmds.select(locGrp)
    cmds.duplicate(n='Locators_Right',rr=True, rc=True)
    cmds.scale(-2,2,2)
    print 'locators created'
    
def createRig():
    master = cmds.circle(nr=(0,1,0), c=(0,0,0),  radius=2, name='Ctrl_Master')	
    
    jntGrp=cmds.group(n='Joints',em=True)
    locs = cmds.ls('loc*', type='transform')
    jnts = []
    ctrls = []
	
    for i, lc in enumerate(locs):
        lPos = cmds.xform(lc, q=True, t=True, ws=True)
        j=cmds.joint(radius=.5, p=lPos, name='jnt_'+str(i))
        jnts.append(j)
        if i == 8:
            cmds.parent(j, 'jnt_0')
    
    cmds.select('jnt_0')
    cmds.joint(e=True, ch=True, oj='xyz', secondaryAxisOrient='yup')
    
    for i, j in enumerate(jnts):
    	jPos = cmds.xform(j, q=True, t=True, ws=True)
    	ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0),  radius=1, name='ctrl_'+str(i))
    	ctrls.append(ctrl)
    	for c in ctrls:
    		cmds.move(jPos[0],jPos[1],jPos[2])
    		cmds.rotate(90,90,0)
    	cmds.makeIdentity(apply=True, t=1, s=1)
    	if i == 0:
    		cmds.parent(ctrl, master)
		
    	else:
    		cmds.parent(ctrl, 'ctrl_'+str(i-1))
    		
        if i == 8:
		    cmds.parent(ctrl, 'ctrl_0')
	cmds.parentConstraint(ctrl, j, mo=True)

def BindSkin():
	cmds.select('bird')
	sel = cmds.ls(selection = True)
	for i in range(0, len(sel)):
		cmds.skinCluster(sel[i], 'jnt_0', bm=3, sm=1, dr=0.1, name='Mesh'+str(i))
		cmds.geomBind('Mesh'+str(i), bm=3, gvp=[256,1], mi=1)
	print 'Skin Bound'
	
    