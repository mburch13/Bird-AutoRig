import maya.cmds as cmds
jnt = 'jnt_'
ctrl = 'ctrl_'
body = ['spine_', 'wing_', 'leg_']
side = ['L_', 'R_']
size = .3

def createSphereCtrl(name):
    cmds.circle(n='yAxis',nr = (0,1,0))
    cmds.circle(n='xAxis', nr = (1,0,0))
    cmds.circle(n='zAxis',nr = (0,0,1))
    cmds.parent('zAxisShape','yAxis', r=True, s=True)
    cmds.parent('xAxisShape','yAxis', r=True, s=True)
    cmds.delete('zAxis')
    cmds.delete('xAxis')
    
    cmds.rename('yAxis', name)
    cmds.rename('zAxisShape', name+'_z')
    cmds.rename('xAxisShape', name+'_x')

def createRig():    
    master = 'ctrl_Master'
    cmds.curve(name=master,bezier=True, d=1, p=[(-1,0,-1),(-1,0,-3),(-2,0,-3),(0,0,-5),(2,0,-3),(1,0,-3),(1,0,-1),(3,0,-1),(3,0,-2),(5,0,0),(3,0,2),(3,0,1),(1,0,1),(1,0,3),(2,0,3),(0,0,5),(-2,0,3),(-1,0,3),(-1,0,1),(-3,0,1),(-3,0,2),(-5,0,0),(-3,0,-2),(-3,0,-1),(-1,0,-1)])
    cmds.setAttr(master+'.overrideEnabled', 1)
    cmds.setAttr(master+'.overrideColor', 16)
    
    jntGrp=cmds.group(n='Joints',em=True)
    root = cmds.ls('loc_root')
    
    rootPos = cmds.xform(root, q = True, t = True, ws = True)
    rootJoint = cmds.joint(radius = size, p = rootPos, name = "jnt_root")

    sJ=[]
    spines = cmds.ls('loc_spine_*', type='locator')
    spine = cmds.listRelatives(*spines, p=True, f=True)
    for i, s in enumerate(spine):
        spinePos = cmds.xform(s, q = True, t = True, ws = True)
        j = cmds.joint(radius =size, p = spinePos, name = jnt + body[0] + str(i))
        sJ.append(j)
    
    lw = []    
    leftWing = cmds.ls('Locators_Left_Wing')
    wingL = cmds.listRelatives(*leftWing, c=True, f=True)
    for i, w in enumerate(wingL):
        wingPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=wingPos, name = jnt+side[0]+body[1]+str(i))
        lw.append(j)
        if i==0:
            cmds.parent(j, rootJoint)

    rw = []
    rightWing = cmds.ls('Locators_Right_Wing')
    wingR = cmds.listRelatives(*rightWing, c=True, f=True)
    for i, w in enumerate(wingR):
        wingPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=wingPos, name = jnt+side[1]+body[1]+str(i))
        rw.append(j)
        if i==0:
            cmds.parent(j, rootJoint)

    lL = []        
    leftLeg = cmds.ls('Locators_Left_Leg')
    legL = cmds.listRelatives(*leftLeg, c=True, f=True)
    for i, w in enumerate(legL):
        legPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=legPos, name = jnt+side[0]+body[2]+str(i))
        lL.append(j)
        if i==0:
            cmds.parent(j, jnt+body[0]+'1')
    
    lR = []        
    rightLeg = cmds.ls('Locators_Right_Leg')
    legR = cmds.listRelatives(*rightLeg, c=True, f=True)
    for i, w in enumerate(legR):
        legPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=legPos, name = jnt+side[1]+body[2]+str(i))
        lR.append(j)
        if i==0:
            cmds.parent(j, jnt+body[0]+'1')
    
    #cmds.select(rootJoint)
    #cmds.joint(e=True, ch=True, oj='xyz', secondaryAxisOrient='yup')
    
    #######ik_handles#####
    cmds.ikHandle(name="ik_L_upper_wing", sj=cmds.ls("jnt_L_wing_0")[0], ee=cmds.ls('jnt_L_wing_2')[0], sol='ikRPsolver')
    lLowW = cmds.ikHandle(name="ik_L_lower_wing", sj=cmds.ls("jnt_L_wing_1")[0], ee=cmds.ls('jnt_L_wing_3')[0], sol='ikRPsolver')
    
    cmds.ikHandle(name="ik_R_upper_wing", sj=cmds.ls("jnt_R_wing_0")[0], ee=cmds.ls('jnt_R_wing_2')[0], sol='ikRPsolver')
    cmds.ikHandle(name="ik_R_lower_wing", sj=cmds.ls("jnt_R_wing_1")[0], ee=cmds.ls('jnt_R_wing_3')[0], sol='ikRPsolver')
    
    #######controls#######
    root = ctrl+'root'
    cPos = cmds.xform(rootJoint, q=True, t=True, ws=True)
    cmds.circle(c = (0,0,0), radius = 1, degree = 1, s = 8, name = root)
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.rotate(-45, 0,0)
    cmds.setAttr(root+'.overrideEnabled', 1)
    cmds.setAttr(root+'.overrideColor', 17)
    cmds.makeIdentity(root, apply=True, t=1,r=1, s=1)
    cmds.parent(root, master)
    
    sC=[]
    for i, j in enumerate(sJ):
        name = ctrl+body[0]+str(i)
        cPos = cmds.xform(j, q=True, t=True, ws=True)
        ctrls = cmds.circle(c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
        sC.append(ctrls)
        for c in sC:
            cmds.move(cPos[0],cPos[1],cPos[2])
            cmds.rotate(-45, 0,0)
        cmds.setAttr(name+'.overrideEnabled', 1)
        cmds.setAttr(name+'.overrideColor', 17)
        cmds.makeIdentity(name, apply=True, t=1, r=1, s=1)
        if i==0:
            cmds.parent(ctrls, root)
        else:
            cmds.parent(ctrls, ctrl+body[0]+str(i-1))
        cmds.parentConstraint(name, j, mo=True)
            
    lShoulder=ctrl+side[0]+'shoulder'
    cPos = cmds.xform(jnt+side[0]+body[1]+'0', q=True, t=True, ws=True)
    createSphereCtrl(lShoulder)
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(lShoulder, apply=True, t=1,r=1, s=1)
    cmds.setAttr(lShoulder+'.overrideEnabled', 1)
    cmds.setAttr(lShoulder+'.overrideColor', 13)
    cmds.parent(lShoulder, root)
    
    lWing=ctrl+side[0]+'wing'
    cPos = cmds.xform(jnt+side[0]+body[1]+'3', q=True, t=True, ws=True)
    cmds.curve(n=lWing, d=1, p=[(-0.707107,0,0.707107),(0.707107,0,0.707107),(0.707107,0,-0.707107),(-0.707107,0,-0.707107),(-0.707107,0,0.707107),(0,1,0),(0.707107,0,-0.707107),(0,-1,0),(-0.707107,0,-0.707107),(0,1,0),(0.707107,0,0.707107),(0,-1,0),(-0.707107,0,0.707107)])
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(lWing, apply=True, t=1,r=1, s=1)
    cmds.setAttr(lWing+'.overrideEnabled', 1)
    cmds.setAttr(lWing+'.overrideColor', 13)
    cmds.parent("ik_L_upper_wing", lWing)
    cmds.parent('ik_L_lower_wing', lWing)
    cmds.parent(lWing, lShoulder)
    
    rShoulder=ctrl+side[1]+'shoulder'
    cPos = cmds.xform(jnt+side[1]+body[1]+'0', q=True, t=True, ws=True)
    createSphereCtrl(rShoulder)
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(rShoulder, apply=True, t=1,r=1, s=1)
    cmds.setAttr(rShoulder+'.overrideEnabled', 1)
    cmds.setAttr(rShoulder+'.overrideColor', 6)
    cmds.parent(rShoulder, root)
    
    rWing=ctrl+side[1]+'wing'
    cPos = cmds.xform(jnt+side[1]+body[1]+'3', q=True, t=True, ws=True)
    cmds.curve(n=rWing, d=1, p=[(-0.707107,0,0.707107),(0.707107,0,0.707107),(0.707107,0,-0.707107),(-0.707107,0,-0.707107),(-0.707107,0,0.707107),(0,1,0),(0.707107,0,-0.707107),(0,-1,0),(-0.707107,0,-0.707107),(0,1,0),(0.707107,0,0.707107),(0,-1,0),(-0.707107,0,0.707107)])
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(rWing, apply=True, t=1,r=1, s=1)
    cmds.setAttr(rWing+'.overrideEnabled', 1)
    cmds.setAttr(rWing+'.overrideColor', 6)
    cmds.parent('ik_R_upper_wing', rWing)
    cmds.parent('ik_R_lower_wing', rWing)
    cmds.parent(rWing, rShoulder)

    cmds.ikHandle(name = "ik_L_leg", sj = cmds.ls("jnt_L_leg_0")[0], ee = cmds.ls("jnt_L_leg_2")[0], sol = "ikRPsolver")
    footPos = cmds.xform('jnt_L_leg_2', q=True, t=True, ws=True)
    name = ctrl+side[0]+'foot'
    foot=cmds.circle(nr=(0,1,0),c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
    cmds.move(footPos[0], footPos[1], footPos[2])
    cmds.scale(.5,1,1)
    cmds.makeIdentity(name, apply=True, t=1, r=1, s=1)
    cmds.parent(foot, master)
    cmds.parent('ik_L_leg', foot)
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideColor', 13)
    
    cmds.ikHandle(name = "ik_R_leg", sj = cmds.ls("jnt_R_leg_0")[0], ee = cmds.ls("jnt_R_leg_2")[0], sol = "ikRPsolver")
    footPos = cmds.xform('jnt_R_leg_2', q=True, t=True, ws=True)
    name = ctrl+side[1]+'foot'
    foot=cmds.circle(nr=(0,1,0),c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
    cmds.move(footPos[0], footPos[1], footPos[2])
    cmds.scale(.5,1,1)
    cmds.makeIdentity(name, apply=True, t=1, r=1, s=1)
    cmds.parent(foot, master)
    cmds.parent('ik_R_leg', foot)
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideColor', 6)

    cmds.parent(jntGrp,master)
def BindSkin():
    cmds.setAttr("ik_R_leg.visibility", 0)
    cmds.setAttr("ik_L_leg.visibility", 0)
    cmds.setAttr("ik_L_upper_wing.visibility", 0)
    cmds.setAttr("ik_L_lower_wing.visibility", 0)
    cmds.setAttr("ik_R_upper_wing.visibility", 0)
    cmds.setAttr("ik_R_lower_wing.visibility", 0)
    cmds.setAttr('Joints.visibility', 0)
    cmds.delete('loc*')

    cmds.select('bird')
    sel = cmds.ls(selection = True)
    for i in range(0, len(sel)):
    	cmds.skinCluster(sel[i], 'jnt_root', bm=3, sm=1, dr=0.1, name='Mesh'+str(i))
    	cmds.geomBind('Mesh'+str(i), bm=3, gvp=[256,1], mi=2)
    	
	cmds.deformerWeights('skinWeights.xml',im=True, sh='bird')
    print 'Skin Bound'
