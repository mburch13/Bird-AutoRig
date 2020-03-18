#create rig
import maya.cmds as cmds
global size
global name

def returnName():
	return cmds.textFieldGrp(name, q = True, text = True)

def returnSize():
	return cmds.intSliderGrp(size, q = True, value = True)

def createRig(objName, objSize):
	createLocators(objSize)
	createJoints()
	bindMesh(objName)
	
def createLocators(objSize):	
	global size
	size = objSize
	size = returnSize()
	if cmds.objExists('Loc'):
		print 'Already Exists'
	else:
		cmds.group(em=True, name='Loc')
	
	for i in range(size+1):
		chain = cmds.spaceLocator(n='loc_'+str(i))
		cmds.move(0, i, 0)
		if i == 0:
			cmds.parent(chain, 'Loc')
		else:
			cmds.parent(chain, 'loc_'+str(i-1))
	
def createJoints():
	master = cmds.circle(nr=(0,1,0), c=(0,0,0),  radius=2, name='Ctrl_Master')	

	jntGrp = cmds.group(em=True, name='Jnts')
	locs = cmds.ls('loc_*', type='transform')
	jnts = []
	ctrls = []
	
	for i,lc in enumerate(locs):
		locPos = cmds.xform(lc, q=True, t=True, ws=True)
		j = cmds.joint(radius=.5, p=locPos, name='jnt_'+str(i))
		jnts.append(j)

	cmds.select('jnt_0')
	cmds.joint(e=True, ch=True, oj='xyz', secondaryAxisOrient='yup')
	

	jnts = cmds.ls('jnt_*', type='transform')
	for i, j in enumerate(jnts):
		jPos = cmds.xform(j, q=True, t=True, ws=True)
		ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0),  radius=1, name='ctrl_'+str(i))
		ctrls.append(ctrl)
		for c in ctrls:
			cmds.move(jPos[0],jPos[1],jPos[2])
		cmds.makeIdentity(apply=True, t=1, s=1)
		if i == 0:
			cmds.parent(ctrl, master)
		else:
			cmds.parent(ctrl, 'ctrl_'+str(i-1))
		cmds.parentConstraint(ctrl, j, mo=True)

def bindMesh(objName):
	global name
	name = objName
	name = returnName()
	sel = cmds.ls(name)
	for i in range(0, len(sel)):
		cmds.skinCluster(sel[i], 'jnt_0', bm=3, sm=1, dr=0.1, name='Mesh'+str(i))
		cmds.geomBind('Mesh'+str(i), bm=3, gvp=[256,1], mi=1)
	print 'Skin Bound'
	

	
	
	