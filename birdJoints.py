import maya.cmds as cmds

#set prefixes for easy naming
jnt = 'jnt_'
ctrl = 'ctrl_'
body = ['spine_', 'wing_', 'leg_']
side = ['L_', 'R_']
size = .3 #set the size of the joints

#creates a gyrosphere control for the wings
def createSphereCtrl(name):
    #create and name nurbs circles and orient them for each axis
    cmds.circle(n='yAxis',nr = (0,1,0))
    cmds.circle(n='xAxis', nr = (1,0,0))
    cmds.circle(n='zAxis',nr = (0,0,1))
    #parent the shape node of the x and z circles under the node of the y circle
    cmds.parent('zAxisShape','yAxis', r=True, s=True)
    cmds.parent('xAxisShape','yAxis', r=True, s=True)
    #delete the unused nodes
    cmds.delete('zAxis')
    cmds.delete('xAxis')

    #rename the main cotroler to the name passed through the functions argument
    cmds.rename('yAxis', name)
    cmds.rename('zAxisShape', name+'_z')
    cmds.rename('xAxisShape', name+'_x')

def createRig():
    #create the master controler and set the color to white
    master = 'ctrl_Master'
    cmds.curve(name=master,bezier=True, d=1, p=[(-1,0,-1),(-1,0,-3),(-2,0,-3),(0,0,-5),(2,0,-3),(1,0,-3),(1,0,-1),(3,0,-1),(3,0,-2),(5,0,0),(3,0,2),(3,0,1),(1,0,1),(1,0,3),(2,0,3),(0,0,5),(-2,0,3),(-1,0,3),(-1,0,1),(-3,0,1),(-3,0,2),(-5,0,0),(-3,0,-2),(-3,0,-1),(-1,0,-1)])
    cmds.setAttr(master+'.overrideEnabled', 1)
    cmds.setAttr(master+'.overrideColor', 16)

    #create joint group
    jntGrp=cmds.group(n='Joints',em=True)

    #access the location of the root locator and create the root joint
    root = cmds.ls('loc_root')
    rootPos = cmds.xform(root, q = True, t = True, ws = True)
    rootJoint = cmds.joint(radius = size, p = rootPos, name = "jnt_root")


    sJ=[] #create array for the spine joints
    #access the spine locators
    spines = cmds.ls('loc_spine_*', type='locator')
    spine = cmds.listRelatives(*spines, p=True, f=True)
    #iterate through the spine locators and create a joint at each location
    #using a iterative naming convention (i.e. jnt_spine_0)
    for i, s in enumerate(spine):
        spinePos = cmds.xform(s, q = True, t = True, ws = True)
        j = cmds.joint(radius =size, p = spinePos, name = jnt + body[0] + str(i))
        sJ.append(j) #add joint to the array

    lw = [] #create array for the left wing joints
    leftWing = cmds.ls('Locators_Left_Wing')
    #access the left wing locators
    wingL = cmds.listRelatives(*leftWing, c=True, f=True)
    #iterate through the left wing locators and create a joint at each location
    #using a iterative naming convention (i.e. jnt_L_wing_0)
    for i, w in enumerate(wingL):
        wingPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=wingPos, name = jnt+side[0]+body[1]+str(i))
        lw.append(j) #add joint to the array
        #correct parenting hierarchy
        if i==0:
            #reparent the first wing joint to the root joint
            cmds.parent(j, rootJoint)

    rw = [] #create array for the right wing joints
    rightWing = cmds.ls('Locators_Right_Wing')
    #access the right wing locators
    wingR = cmds.listRelatives(*rightWing, c=True, f=True)
    #iterate through the right wing locators and create a joint at each location
    #using a iterative naming convention (i.e. jnt_R_wing_0)
    for i, w in enumerate(wingR):
        wingPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=wingPos, name = jnt+side[1]+body[1]+str(i))
        rw.append(j) #add joint to the array
        #correct parenting hierarchy
        if i==0:
            #reparent the first wing joint to the root joint
            cmds.parent(j, rootJoint)

    lL = [] #create array for the left leg joints
    leftLeg = cmds.ls('Locators_Left_Leg')
    #access the right wing locators
    legL = cmds.listRelatives(*leftLeg, c=True, f=True)
    #iterate through the left leg locators and create a joint at each location
    #using a iterative naming convention (i.e. jnt_L_leg_0)
    for i, w in enumerate(legL):
        legPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=legPos, name = jnt+side[0]+body[2]+str(i))
        lL.append(j) #add joint to the array
        #correct parenting hierarchy
        if i==0:
            #reparent the first wing joint to the root joint
            cmds.parent(j, jnt+body[0]+'1')

    lR = [] #create array for the left leg joints
    rightLeg = cmds.ls('Locators_Right_Leg')
    #access the right wing locators
    legR = cmds.listRelatives(*rightLeg, c=True, f=True)
    #iterate through the rigth leg locators and create a joint at each location
    #using a iterative naming convention (i.e. jnt_R_leg_0)
    for i, w in enumerate(legR):
        legPos = cmds.xform(w, q=True, t=True, ws=True)
        j=cmds.joint(radius=size, p=legPos, name = jnt+side[1]+body[2]+str(i))
        lR.append(j) #add joint to the array
        #correct parenting hierarchy
        if i==0:
            #reparent the first wing joint to the root joint
            cmds.parent(j, jnt+body[0]+'1')

    #orient joints
    cmds.select(rootJoint)
    cmds.joint(e=True, ch=True, oj='xyz', secondaryAxisOrient='yup')

    #######wing ik handles#####
    cmds.ikHandle(name="ik_L_upper_wing", sj=cmds.ls("jnt_L_wing_0")[0], ee=cmds.ls('jnt_L_wing_2')[0], sol='ikRPsolver')
    cmds.ikHandle(name="ik_L_lower_wing", sj=cmds.ls("jnt_L_wing_1")[0], ee=cmds.ls('jnt_L_wing_3')[0], sol='ikRPsolver')

    cmds.ikHandle(name="ik_R_upper_wing", sj=cmds.ls("jnt_R_wing_0")[0], ee=cmds.ls('jnt_R_wing_2')[0], sol='ikRPsolver')
    cmds.ikHandle(name="ik_R_lower_wing", sj=cmds.ls("jnt_R_wing_1")[0], ee=cmds.ls('jnt_R_wing_3')[0], sol='ikRPsolver')

    #######create controls#######
    root = ctrl+'root'
    #access root joint location
    cPos = cmds.xform(rootJoint, q=True, t=True, ws=True)
    #create controler
    cmds.circle(c = (0,0,0), radius = 1, degree = 1, s = 8, name = root)
    #position controler at root joint location
    cmds.move(cPos[0],cPos[1],cPos[2])
    cmds.rotate(-45, 0,0)
    #set the controler color to yellow
    cmds.setAttr(root+'.overrideEnabled', 1)
    cmds.setAttr(root+'.overrideColor', 17)
    #freeze tranformations
    cmds.makeIdentity(root, apply=True, t=1,r=1, s=1)
    #parent to master
    cmds.parent(root, master)

    sC=[] #create spine controler array
    #iterate through the spine joints from the joint array
    for i, j in enumerate(sJ):
        name = ctrl+body[0]+str(i) #create the spine joints names
        cPos = cmds.xform(j, q=True, t=True, ws=True)
        ctrls = cmds.circle(c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
        sC.append(ctrls) #add the controler to the array
        #iterate through the controler array to postition controlers on joints
        for c in sC:
            cmds.move(cPos[0],cPos[1],cPos[2])
            cmds.rotate(-45, 0,0)
        #set the color to yellow
        cmds.setAttr(name+'.overrideEnabled', 1)
        cmds.setAttr(name+'.overrideColor', 17)
        cmds.makeIdentity(name, apply=True, t=1, r=1, s=1) #freeze tranformations
        #correct parenting hierarchy
        if i==0:
            cmds.parent(ctrls, root) #parent the first controler to the root
        else:
            cmds.parent(ctrls, ctrl+body[0]+str(i-1)) #parent the current controler to the previous controler
        cmds.parentConstraint(name, j, mo=True) #parent constrain joints

    lShoulder=ctrl+side[0]+'shoulder' #set left shoulder name
    cPos = cmds.xform(jnt+side[0]+body[1]+'0', q=True, t=True, ws=True) #access left shoulder joint
    createSphereCtrl(lShoulder) #call gyrosphere function
    cmds.move(cPos[0],cPos[1],cPos[2]) #position control on joint
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(lShoulder, apply=True, t=1,r=1, s=1) #freeze tranformations
    #set controler color to red
    cmds.setAttr(lShoulder+'.overrideEnabled', 1)
    cmds.setAttr(lShoulder+'.overrideColor', 13)
    cmds.parent(lShoulder, root)

    lWing=ctrl+side[0]+'wing' #set left wing name
    cPos = cmds.xform(jnt+side[0]+body[1]+'3', q=True, t=True, ws=True) #access left wing tip joint
    #create diamond controler
    cmds.curve(n=lWing, d=1, p=[(-0.707107,0,0.707107),(0.707107,0,0.707107),(0.707107,0,-0.707107),(-0.707107,0,-0.707107),(-0.707107,0,0.707107),(0,1,0),(0.707107,0,-0.707107),(0,-1,0),(-0.707107,0,-0.707107),(0,1,0),(0.707107,0,0.707107),(0,-1,0),(-0.707107,0,0.707107)])
    cmds.move(cPos[0],cPos[1],cPos[2]) #position control on joint
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(lWing, apply=True, t=1,r=1, s=1) #freeze transformations
    #set controler color to red
    cmds.setAttr(lWing+'.overrideEnabled', 1)
    cmds.setAttr(lWing+'.overrideColor', 13)
    #parent wing ik handles to controler
    cmds.parent("ik_L_upper_wing", lWing)
    cmds.parent('ik_L_lower_wing', lWing)
    cmds.parent(lWing, lShoulder)

    rShoulder=ctrl+side[1]+'shoulder' #set right shoulder name
    cPos = cmds.xform(jnt+side[1]+body[1]+'0', q=True, t=True, ws=True)
    createSphereCtrl(rShoulder) #call gyrosphere function
    cmds.move(cPos[0],cPos[1],cPos[2]) #position control on joint
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(rShoulder, apply=True, t=1,r=1, s=1) #freeze tranformations
    #set controler color to blue
    cmds.setAttr(rShoulder+'.overrideEnabled', 1)
    cmds.setAttr(rShoulder+'.overrideColor', 6)
    cmds.parent(rShoulder, root)

    rWing=ctrl+side[1]+'wing'  #set right wing name
    cPos = cmds.xform(jnt+side[1]+body[1]+'3', q=True, t=True, ws=True)
    #create diamond controler
    cmds.curve(n=rWing, d=1, p=[(-0.707107,0,0.707107),(0.707107,0,0.707107),(0.707107,0,-0.707107),(-0.707107,0,-0.707107),(-0.707107,0,0.707107),(0,1,0),(0.707107,0,-0.707107),(0,-1,0),(-0.707107,0,-0.707107),(0,1,0),(0.707107,0,0.707107),(0,-1,0),(-0.707107,0,0.707107)])
    cmds.move(cPos[0],cPos[1],cPos[2]) #position control on joint
    cmds.scale(.5,.5,.5)
    cmds.makeIdentity(rWing, apply=True, t=1,r=1, s=1) #freeze tranformations
    #set controler color to blue
    cmds.setAttr(rWing+'.overrideEnabled', 1)
    cmds.setAttr(rWing+'.overrideColor', 6)
    #parent wing ik handles to controler
    cmds.parent('ik_R_upper_wing', rWing)
    cmds.parent('ik_R_lower_wing', rWing)
    cmds.parent(rWing, rShoulder)

    #create left leg ik handle
    cmds.ikHandle(name = "ik_L_leg", sj = cmds.ls("jnt_L_leg_0")[0], ee = cmds.ls("jnt_L_leg_2")[0], sol = "ikRPsolver")
    footPos = cmds.xform('jnt_L_leg_2', q=True, t=True, ws=True) #access foot joint
    name = ctrl+side[0]+'foot' #set foot name
    #create foot controler
    foot=cmds.circle(nr=(0,1,0),c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
    cmds.move(footPos[0], footPos[1], footPos[2]) #position control on joint
    cmds.scale(.5,1,1)
    cmds.makeIdentity(name, apply=True, t=1, r=1, s=1) #freeze tranformations
    cmds.parent(foot, master)
    cmds.parent('ik_L_leg', foot) #parent leg ik handle to controler
    #set controler color to red
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideColor', 13)

    #create right leg ik handle
    cmds.ikHandle(name = "ik_R_leg", sj = cmds.ls("jnt_R_leg_0")[0], ee = cmds.ls("jnt_R_leg_2")[0], sol = "ikRPsolver")
    footPos = cmds.xform('jnt_R_leg_2', q=True, t=True, ws=True) #access foot joint
    name = ctrl+side[1]+'foot' #set foot name
    #create foot controler
    foot=cmds.circle(nr=(0,1,0),c = (0,0,0), radius = 1, degree = 1, s = 8, name = name)
    cmds.move(footPos[0], footPos[1], footPos[2])
    cmds.scale(.5,1,1)
    cmds.makeIdentity(name, apply=True, t=1, r=1, s=1) #freeze tranformations
    cmds.parent(foot, master)
    cmds.parent('ik_R_leg', foot) #parent leg ik handle to controler
    #set controler color to blue
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideColor', 6)

    #parnet joint group under the master control to allow for uniform scaling
    cmds.parent(jntGrp,master)

def BindSkin():
    #hide all ik handles
    cmds.setAttr("ik_R_leg.visibility", 0)
    cmds.setAttr("ik_L_leg.visibility", 0)
    cmds.setAttr("ik_L_upper_wing.visibility", 0)
    cmds.setAttr("ik_L_lower_wing.visibility", 0)
    cmds.setAttr("ik_R_upper_wing.visibility", 0)
    cmds.setAttr("ik_R_lower_wing.visibility", 0)
    cmds.setAttr('Joints.visibility', 0) #hide joints so animators do not accidently move them
    cmds.delete('loc*') #delete locators

    #bind the bird mesh to the rig using a geodexic voxel bind
    cmds.select('bird')
    sel = cmds.ls(selection = True)
    for i in range(0, len(sel)):
    	cmds.skinCluster(sel[i], 'jnt_root', bm=3, sm=1, dr=0.1, name='Mesh'+str(i))
    	cmds.geomBind('Mesh'+str(i), bm=3, gvp=[256,1], mi=2)

    #import skin weights
	cmds.deformerWeights('skinWeights.xml',im=True, sh='bird')
    print 'Skin Bound'
