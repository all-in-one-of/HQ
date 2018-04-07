#!usr/bin/env python
#coding:utf-8

#----------------------
#
# file:IkCurStretch.py
# write: lsy
# time: 2017.5
#
#----------------------

import maya.cmds as cmds 
import maya.mel as mel
import pymel.core as pm
import maya.OpenMaya as OpenMaya

#---------------------------
#
# class : LsyIkCurStretchUI
#
#---------------------------

class LsyIkCurStretchUI():

	win = "LsyIkCurStretchWindow"
	isg1 = None
	isg2 = None
	isg3 = None
	cb = None
	tfg = None
	
	def __init__(self):
		self.LsyIkCurStretchWin()


	def LsyIkCurStretchWin(self):

		if cmds.window(self.win,exists=1):
			cmds.deleteUI(self.win)

		cmds.window(self.win,t="create IkCurve Strecth")
		f = cmds.formLayout(nd=100,w=450)
		LsyIkCurStretchUI.tfg  = cmds.textFieldGrp("LsyIkCur_textFieldGrp",cw2 =(140,80),l="output Name",tx="name")
		LsyIkCurStretchUI.isg1 = cmds.intSliderGrp("LsyIkCur_IntSliderGrp1",field=1, l="ctrl  Number",v=1,min=3,cc= 'LsyIkCurStretchUI.isg1Command()')
		LsyIkCurStretchUI.isg2 = cmds.intSliderGrp("LsyIkCur_IntSliderGrp2",field=1,l="joint Number",v=9,en=0,min=2,max=1000)
		LsyIkCurStretchUI.isg3 = cmds.intSliderGrp("LsyIkCur_IntSliderGrp3",field=1,cw2=(20,50),v=3,min=1,max=9,cc= 'LsyIkCurStretchUI.isg3Command()')
		LsyIkCurStretchUI.cb = cmds.checkBox("LsyIkCur_checkBox",l="multiple",v=1,ofc='LsyIkCurStretchUI.cbCommand()',onc='LsyIkCurStretchUI.cbCommand()')
		b1 = cmds.button(l="Create",c='LsyIk_doItCurStretch()')
		b2 = cmds.button(l="Cancel",c=('cmds.deleteUI(LsyIkCurStretchUI.win)'))

		cmds.formLayout(f,e=1,af=((self.tfg,"top",10),(self.tfg,"left",30),
								(self.isg1,"top",40),(self.isg1,"left",30),
								(self.isg2,"top",100),(self.isg2,"left",30),
								(self.isg3,"top",64),(self.isg3,"left",90),
								(self.cb,"top",67),(self.cb,"left",30),
								(b1,"top",150),(b1,"left",20),
								(b2,"top",150),(b2,"right",20)),
							  ap=((b1,"right",0,47),(b2,"left",0,52)))

		cmds.showWindow(self.win)


	@classmethod
	def cbCommand(self):
		if cmds.checkBox(self.cb,q=1,v=1):
			cmds.intSliderGrp(self.isg2,e=1,en=0)
			cmds.intSliderGrp(self.isg3,e=1,en=1)
			v = self.sigValue(1)
			i = self.sigValue(3)
			cmds.intSliderGrp(self.isg2,e = 1,v = v*i)
		else:
			cmds.intSliderGrp(self.isg2,e=1,en=1)
			cmds.intSliderGrp(self.isg3,e=1,en=0)


	@classmethod
	def isg1Command(self):
		if cmds.checkBox(self.cb,q=1,v=1):
			v = self.sigValue(1)
			i = self.sigValue(3)
			cmds.intSliderGrp(self.isg2,e = 1,v = v*i)

	@classmethod
	def isg3Command(self):
		i = self.sigValue(3)
		if i%2 == 0:
			cmds.intSliderGrp(self.isg3,e = 1,v = i+1)
		if cmds.checkBox(self.cb,q=1,v=1):
			v = self.sigValue(1)
			cmds.intSliderGrp(self.isg2,e = 1,v = v*i)

	@classmethod
	def sigValue(self,i):
		if i == 1:
			v = cmds.intSliderGrp(self.isg1,q=1,v=1)
		if i == 2:
			v = cmds.intSliderGrp(self.isg2,q=1,v=1)
		if i == 3:
			v = cmds.intSliderGrp(self.isg3,q=1,v=1)
		return v

#--------------------------
#
# compute locate in curve
#
#--------------------------

def IK_getUParam( pnt = [], crv = None):

    point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(IK_getDagPath(crv))
    paramUtill=OpenMaya.MScriptUtil()
    paramPtr=paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:
        
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    else :
        point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    
    param = paramUtill.getDouble(paramPtr)  
    return param

def IK_getDagPath(objectName):
    
    if isinstance(objectName, list)==True:
        oNodeList=[]
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

#-------------------------
#
# create new Curve 
#
#-------------------------

def IK_createAveObj(cur,number,s="group"):

	newCur = pm.duplicate(cur,rr=1,n=cur+"_copyCurve1")
	curInfo = pm.arclen(cur,ch=1)
	ns = int(curInfo.arcLength.get())
	pm.delete(curInfo)
	pm.rebuildCurve(newCur,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=ns*100,d=3,tol=0.01)

	allNewInfo = []
	aimObj = []

	p = 1.0 / float((number-1))
	prF = 0.0

	if s == "position":
		allPoistion = []

	for i in range(number):
		if i == number-1:
			NewInfo = pm.pointOnCurve(newCur,ch=1,top=1,pr=1)
		else:
			NewInfo = pm.pointOnCurve(newCur,ch=1,top=1,pr=prF)
			prF+=p
		allNewInfo.append(NewInfo)

		t =pm.getAttr(NewInfo+".position")

		if s == "position":
			allPoistion.append(t)

		if s == "group":
			obj = pm.group(em=1,n=cur+"_AimGrp"+str(i+1))
			aimObj.append(obj)
			pm.setAttr(obj+".translate",t)
			cmds.select(cl=1)

	pm.delete(allNewInfo,newCur)

	if s == "position":
		return allPoistion

	if s == "group":
		return aimObj

def IK_objPosition(cur,obj):
	
	vec =[]
	crv= str(pm.ls(cur)[0].listRelatives(s=1)[0])
	u = [IK_getUParam(cmds.xform(str(obj[i-1]),q=1,ws=1,t=1), crv) for i in range(1,len(obj)+1)]
	
	l = u[-1]
	cv =[u[0],]
	
	for i in range(1,len(u)-1):
		cv.append(((u[i]-u[i-1])*0.5)+u[i-1])
		cv.append(((u[i]-u[i-1])*0.9)+u[i-1])
		cv.append(u[i])
		cv.append(((u[i+1]-u[i])*0.1)+u[i])
	if len(u) > 1:
		cv.append(((u[-1]-u[-2])*0.5)+u[-2])
	cv.append(l)
	
	ii=1
	for p in cv:
		po = pm.pointOnCurve(cur,ch=1,pr=p)
		info = pm.rename(po,cur+"_curveInfo"+str(i))

		vec.append(info.getAttr("position"))
		pm.delete(info)
		ii +=1
	pm.delete(obj)
	return vec
	

#-------------------------
#
# create joint line
#
#-------------------------

def LsyIk_createJointLine(cur,number,jointName):

	numberPosition = IK_createAveObj(cur,number,s="position")

	allJoint = []

	for i in range(0,len(numberPosition)):

		j = jointName +"_joint"+str(i+1)

		if i == 0:
			cmds.joint(n=j,p=numberPosition[i])
			allJoint.append(j)
		else:
			frontJoint =jointName +"_joint"+str(i)
			cmds.joint(n=j,p=numberPosition[i])
			cmds.joint(frontJoint,e=1,zso=1,oj="xyz",sao="zup",ch=1)
			allJoint.append(j)

		if i == len(numberPosition)-1:
			cmds.joint(j,e=1,oj="none",ch=1,zso=1)

	return allJoint

#------------------------------------
# 
# class : LsyIk_ctrlToSkinClass
# create ctrlSkinJoint skin to curve
#
#------------------------------------

class LsyIk_ctrlToSkinClass(object):

	def __init__(self):
		self.AllSkinJoint = []
		self.AllCtrlGro = []

	@staticmethod
	def LsyIk_group(obj):

		c = cmds.group(n=obj+"_C",em=1)
		g = cmds.group(n=obj+"_G",em=1)
		cmds.parent(c,g)

		par = cmds.parentConstraint(obj,g,weight=1)
		cmds.delete(par)
		cmds.parent(obj,c)

		return g

	def LsyIk_createSkinJoint(self,obj):

		cmds.select(cl=1)
		skinJoint = obj + "_skinJoint"
		cmds.joint(n= skinJoint,p=(0,0,0))
		g = cmds.group(n = skinJoint+"_G",em=1)
		cmds.parent(skinJoint,g)

		par = cmds.parentConstraint(obj,g,weight=1)
		cmds.delete(par)
		cmds.parent(g,obj)
		cmds.setAttr(g+".v",0)

		return skinJoint

	def LsyIk_createCtrl(self,name,i=0):

		criclePoint=[(-0.999999983,-0.0001821259143,-1.608122622e-016),
					 (-0.9999674614,-0.1745790446,-1.608070324e-016),
					 (-0.9064639959,-0.5234173324,-1.457705283e-016),
					 (-0.5233728906,-0.9065084378,-8.416477995e-017),
					 (-5.766767883e-016,-1.046745781,-5.536002986e-032),
					 (0.5233728906,-0.9065084378,8.416477995e-017),
					 (0.9065084378,-0.5233728906,1.457776751e-016),
					 (1.046745781,-8.931418499e-016,1.683295599e-016),
					 (0.9065084378,0.5233728906,1.457776751e-016),
					 (0.5364781395,0.8934031888,8.627226471e-017),
					 (0.1928598067,0.9950552101,3.101422233e-017),
					 (0.001386821245,0.9999996446,1.084202172e-019),
					 (0.001386573934,0.9999996596,-3.10553313e-005),
					 (2.113960203e-016,1.000075159,-0.1741771318),
					 (1.692379612e-016,0.9065084378,-0.5233728906),
					 (6.070449388e-017,0.5233728906,-0.9065084378),
					 (-6.409469352e-017,-2.967277895e-016,-1.046745781),
					 (-1.717197595e-016,-0.5233728906,-0.9065084378),
					 (-2.333326547e-016,-0.9065084378,-0.5233728906),
					 (-2.324242534e-016,-1.046745781,-3.442525349e-016),
					 (-1.692379612e-016,-0.9065084378,0.5233728906),
					 (-6.070449388e-017,-0.5233728906,0.9065084378),
					 (6.409469352e-017,-6.607175965e-016,1.046745781),
					 (1.717197595e-016,0.5233728906,0.9065084378),
					 (2.312458705e-016,0.8935319138,0.5363494146),
					 (2.327564702e-016,0.9951594037,0.1924913138),
					 (0.001386821245,0.9999996446,1.827003333e-019),
					 (0.001386821245,0.9999996446,1.54924007e-019),
					 (-0.1740012903,1.000122276,-2.79815416e-017),
					 (-0.5233728906,0.9065084378,-8.416477995e-017),
					 (-0.9065084378,0.5233728906,-1.457776751e-016),
					 (-1.00001464,0.1744029924,-1.608146193e-016),
					 (-0.9999999949,-0.000115346413,-1.608122641e-016),
					 (-0.9999999808,1.185947312e-020,-0.0001936798941),
					 (-0.9999999942,7.510999686e-021,-0.0001226639337),
					 (-1.000015569,-1.067889108e-017,0.1743995262),
					 (-0.9065084378,-3.204734676e-017,0.5233728906),
					 (-0.5233728906,-5.550763283e-017,0.9065084378),
					 (-6.607175965e-016,-6.409469352e-017,1.046745781),
					 (0.5233728906,-5.550763283e-017,0.9065084378),
					 (0.9065084378,-3.204734676e-017,0.5233728906),
					 (1.046745781,-6.043388073e-032,9.869601712e-016),
					 (0.9065084378,3.204734676e-017,-0.5233728906),
					 (0.5233728906,5.550763283e-017,-0.9065084378),
					 (-2.967277895e-016,6.409469352e-017,-1.046745781),
					 (-0.5233728906,5.550763283e-017,-0.9065084378),
					 (-0.9064611766,3.205024067e-017,-0.5234201517),
					 (-0.9999653969,1.069035504e-017,-0.1745867469),
					 (-0.9999999808,1.185947312e-020,-0.0001936798941)]

		if i == 0:
			point = criclePoint

		ctrlName = cmds.curve(n = name + "_ctrl",d=3,p=point)

		return ctrlName

	def LsyIK_setCurSkinWeight(self,jointName,skin,cvName):

		value = 1.0 / float(len(jointName))
		numTv = []

		for j in range(0,len(jointName)):
			numTv.append((jointName[j],value))

		cmds.skinPercent(skin,cvName,tv = numTv)

	def LsyIK_doItCtrl(self,cur,outputName,numJoint):

		for i in range(0,len(numJoint)):

			ctrl = self.LsyIk_createCtrl(name = outputName + str(i+1))
			ctrl_G = self.LsyIk_group(ctrl)
			self.AllCtrlGro.append(ctrl_G)

			self.AllSkinJoint.append(self.LsyIk_createSkinJoint(ctrl))

			par = cmds.parentConstraint(numJoint[i],ctrl_G,weight=1)
			cmds.delete(par)

		skinName = cmds.skinCluster(self.AllSkinJoint,cur,tsb=1,weight=1)

		curShape = pm.listRelatives(cur,shapes=1)[0]
		curCVs = []
		for cv in range(0,curShape.numCVs()):
			curCVs.append(cur + ".cv[" + str(cv) + "]")

		n = len(self.AllSkinJoint)
		
		for j in range(0,n):

			if j == 0:
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[j])

			if 0 < j < n-1:
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j-1],self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[4*j-3])
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[4*j-2])
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[4*j-1])
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[4*j])
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j],self.AllSkinJoint[j+1]],skin=skinName[0],cvName = curCVs[4*j+1])

			if j == n-1:
				self.LsyIK_setCurSkinWeight(jointName=[self.AllSkinJoint[j]],skin=skinName[0],cvName = curCVs[-1])



#-------------------------
#
# create ikCurve Stretch
#
#-------------------------

def LsyIK_stretch(cur,obj,scaleObj):
	
	crv= str(pm.ls(cur)[0].listRelatives(s=1)[0])
	u = [IK_getUParam(cmds.xform(str(obj[i-1]),q=1,ws=1,t=1), crv) for i in range(1,len(obj)+1)]
	info = []
	for i in range(len(u)):
		po = pm.pointOnCurve(cur,ch=1,pr=u[i])
		info.append(pm.rename(po,cur+"_curveInfo"+str(i)))
	
	t = [i for i in range(0,len(info)-1,2)]
	for i in range(0,len(info)-1):
		
		dis = pm.createNode("distanceBetween",n=obj[i+1]+"_disBet")
		pm.connectAttr(info[i]+".position",dis+".point1")
		pm.connectAttr(info[i+1]+".position",dis+".point2")
		
		if i in t:
			mul = [pm.createNode("multiplyDivide",n=obj[i+1]+"_mul"+x) for x in ["1","2"] ]
			[pm.setAttr(s+".operation",2) for s in mul]
			
			pm.connectAttr(dis+".distance",mul[0]+".input1X")
			pm.connectAttr(scaleObj+".sy",mul[0]+".input2X")
			
			pm.connectAttr(mul[0]+".outputX",mul[1]+".input1X")
			pm.setAttr(mul[1]+".input2X",pm.getAttr(mul[1]+".input1X"))
			pm.connectAttr(mul[1]+".outputX",obj[i]+".sx")
		else:
			pm.connectAttr(dis+".distance",mul[0]+".input1Z")
			pm.connectAttr(scaleObj+".sy",mul[0]+".input2Z")
			
			pm.connectAttr(mul[0]+".outputZ",mul[1]+".input1Z")
			pm.setAttr(mul[1]+".input2Z",pm.getAttr(mul[1]+".input1Z"))
			pm.connectAttr(mul[1]+".outputZ",obj[i]+".sx")

def LsyEval_IK_stretch(scaleObj,IkCur,Joint):
	'''
	sl = cmds.ls(sl=1)
	if len(sl) != 2:
		cmds.error("先选择IK曲线，再选择IK头骨�?)
	if cmds.nodeType(cmds.listRelatives(sl[0],s=1)[0]) != "nurbsCurve":
		cmds.error("先选择IK曲线，再选择IK头骨�?)
	if cmds.nodeType(sl[1]) != "joint":
		cmds.error("先选择IK曲线，再选择IK头骨�?)
	'''
	sl = [IkCur,Joint]
	s = pm.listRelatives(sl[1],ad=1)
	allJoint = [x for x in s if type(x) == pm.nodetypes.Joint]
	allJoint.append(sl[1])
	allJoint.reverse()
	
	LsyIK_stretch(sl[0],allJoint,scaleObj)

#-------------------------
#
# doIt ikCurStretch  
#
#--------------------------

def LsyIk_doItCurStretch(*args):

	cur = cmds.ls(sl=1)
	if len(cur) < 2:
		cmds.error("First select to IK curves,next select to scale curves")

	v = cmds.intSliderGrp(LsyIkCurStretchUI.isg1,q=1,v=1)
	j = cmds.intSliderGrp(LsyIkCurStretchUI.isg2,q=1,v=1)
	attr = ["t","r","s"]
	xyz = ["x","y","z"]
	objAttr = [x+y for x in attr for y in xyz ]	

	for i in range(len(cur)-1):

		# input error
		if cmds.listRelatives(cur[i],p=1) != None:
			cmds.error(cur[i]+" getup have to group")

		for x in range(0,5):
			if cmds.getAttr(cur[i]+"."+objAttr[x]) != 0:
				cmds.error(cur[i]+"."+objAttr[x] + " value not 0")

		for x in range(6,8):
			if cmds.getAttr(cur[i]+"."+objAttr[x]) != 1:
				cmds.error(cur[i]+"."+objAttr[x] + " value not 1")

		# get ctrl && joint Name
		if (len(cur)-1) < 2:
			name = cmds.textFieldGrp(LsyIkCurStretchUI.tfg,q=1,tx=1)
		else:
			name = cmds.textFieldGrp(LsyIkCurStretchUI.tfg,q=1,tx=1) + str(i+1)

		ctrlName = name + "_ctrl" 
		jointName = name + "_Ik"
		newCur = name + "_curve"

		# create new Curve 
		loc = IK_createAveObj(cur = cur[i],number = v,s="group")
		ve = IK_objPosition(cur[i],loc)
		newIkCur = cmds.curve(n=newCur,d=3,p=ve)
		
		# create number joint
		allJoint = LsyIk_createJointLine(newCur,j,jointName)

		# create IKHandle
		newIK = cmds.ikHandle(n=newCur+"_ikHandle",sj=allJoint[0],ee=allJoint[-1],c=newCur,ccv=0,pcv=0,sol="ikSplineSolver")[0]
		print newIK

		# create number ctrl && curve skin
		ctrlJoint = LsyIk_createJointLine(newCur,v,(jointName+"ctrl"))
		cc = LsyIk_ctrlToSkinClass()
		cc.LsyIK_doItCtrl(newCur,ctrlName,ctrlJoint)
		cmds.delete(ctrlJoint)

		# create IK_stretch
		LsyEval_IK_stretch(cur[-1],newCur,allJoint[0])

		newGro = cmds.group(em=1,n=name+"_ikHandle_G")
		cmds.parent((newIkCur,newIK),newGro)
		cmds.setAttr(newIkCur+".v",0)
		cmds.setAttr(newIK+".v",0)

		jGro = cmds.group(em=1,n=name+"_Ik_joint_G")
		cmds.parent(allJoint[0],jGro)

		ikGro = cmds.group(em=1,n=name+"_Ik_G")
		cmds.parent(jGro,ikGro)
		cmds.parent(cc.AllCtrlGro,ikGro)
		
	cmds.select(cl=1)
	print "create ----------------- *****  ok  ***********",
#def IkCurStretch():
if __name__=='__main__':
	LsyIkCurStretchUI()