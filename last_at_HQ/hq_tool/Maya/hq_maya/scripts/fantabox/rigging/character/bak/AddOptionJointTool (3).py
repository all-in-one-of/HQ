#!usr/bin/env python
#coding: utf-8

#--------------------------------
# file : AddOptionJointTool
# write :lsy
# time:2017.6
#--------------------------------

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as  pm

#------------------------
#
#optionUIClass
#
#------------------------
class optionUIClass(object):

	cb1 = "optionUI_checkBox1"
	cb2 = "optionUI_checkBox2" 
	cbY = "optionUI_checkBoxY"
	cbZ = "optionUI_checkBoxZ"
	cbM = "optionUI_checkBoxM"
	button1 = "optionUI_button1"
	button1_1 = "optionUI_button1_1"
	button2 = "optionUI_button2"
	button3 = "optionUI_button3"
	button4 = "optionUI_button4"
	buttonFollow1 = "optionUI_buttonFollow1"
	buttonFollow2 = "optionUI_buttonFollow2"
	buttonFollow3 = "optionUI_buttonFollow3"
	setLayout = "optionUI_setLayout"
	cb_value = True
	YZ_value = 3
	Mirror_value = False
	
	def __init__(self):
		self.optionUI()
	
	@classmethod
	def optionUI(cls,winName ="optionWinUI"):
		if cmds.window(winName,ex=1):
			cmds.deleteUI(winName)

		cmds.window(winName,t="添加辅助骨骼")
		cmds.columnLayout(adj=1)
		cmds.text(l="",w=20,h=10)
		cmds.setParent("..")
		cmds.rowColumnLayout(w=200,h=30,nc=4)
		cmds.text(l="",w=25,h=10)
		cmds.checkBox(optionUIClass.cb1,v=1,label='十字骨骼',cc= 'optionUIClass.cb_command()' )
		cmds.text(l="",w=35,h=10)
		cmds.checkBox(optionUIClass.cb2,v=0,label='一字骨骼',cc= 'optionUIClass.cb_command()' )
		cmds.setParent("..")
		cmds.rowColumnLayout(nbg=1,nc=2,h=100)
		cmds.text(l="",w=35)
		cmds.button(optionUIClass.button1,l="创建骨骼",w=120,h=40,c='optionUIClass.button1_command()')
		cmds.text(l="",w=20)
		cmds.text(l="",w=20)
		cmds.text(l="",w=35)
		cmds.button(optionUIClass.button1_1,l="重新定位骨骼",w=120,h=40,c='optionJointClass.option_LocatorJoint()')
		cmds.text(l="",w=20)
		cmds.text(l="",w=20)
		cmds.setParent("..")
		cmds.separator()
		cmds.rowColumnLayout(nbg=1,nc=2)
		cmds.text(l="",w=80)
		cmds.checkBox(optionUIClass.cbM,v=0,w=120,h=30,label='Mirror', cc = 'optionUIClass.cb_M_command()')
		cmds.setParent("..")
		cmds.rowColumnLayout(nbg=1,nc=4,)
		cmds.text(l="",w=55)
		cmds.checkBox(optionUIClass.cbY,v=1,w=30,h=20,label='Y', cc = 'optionUIClass.cb_YZ_command()')
		cmds.text(l="",w=30)
		cmds.checkBox(optionUIClass.cbZ,v=1,w=30,h=20,label='Z', cc = 'optionUIClass.cb_YZ_command()')
		cmds.setParent("..")
		cmds.rowColumnLayout(h=50,nbg=1,nc=4)
		cmds.text(l="",w=35)
		cmds.button(optionUIClass.button2,l="关联辅助骨骼",w=120,h=40,c='optionJointClass.optionJointLine()')
		cmds.setParent("..")
		cmds.separator()
		cmds.text(l="设置...",w=10,h=30)
		cmds.rowColumnLayout(optionUIClass.setLayout,nbg=1,nc=5,h=50)
		cmds.text(l="",w=20)
		cmds.button(optionUIClass.buttonFollow1,h=35,w=70,l="十字骨骼设置",c = 'option_setUI()')
		cmds.text(l="",w=5)
		cmds.button(optionUIClass.buttonFollow2,h=35,w=70,l="选择蒙皮骨骼", c = 'Option_SelectToSkinJoint()')
		cmds.text(l="",w=10)
		cmds.setParent("..")
		cmds.separator()
		cmds.rowColumnLayout(nbg=1,nc=2,h=120)
		cmds.text(l="",w=20)
		cmds.text(l="",w=20)
		cmds.text(l="",w=35)
		cmds.button(optionUIClass.button3,l="添加ADV辅助骨骼",w=120,h=40,c='doItAddAdvOptionJoint()')
		cmds.text(l="",h=5)
		cmds.text(l="",h=5)
		cmds.text(l="",w=35)
		cmds.button(optionUIClass.button4,l="关联ADV辅助骨骼",w=120,h=40,c='doItAddAdvOptionJointLine()')
		cmds.showWindow(winName)
	
	@classmethod 
	def cb_command(cls):
		if optionUIClass.cb_value:
			cmds.checkBox(optionUIClass.cb1,e=1,v=0)
			cmds.checkBox(optionUIClass.cb2,e=1,v=1)
			optionUIClass.cb_value = False

			cmds.checkBox(optionUIClass.cbY,e=1,en=0)
			cmds.checkBox(optionUIClass.cbZ,e=1,en=0)
			#cmds.rowColumnLayout(optionUIClass.setLayout,e=1,en=0)
		else:
			cmds.checkBox(optionUIClass.cb1,e=1,v=1)
			cmds.checkBox(optionUIClass.cb2,e=1,v=0)
			optionUIClass.cb_value = True

			cmds.checkBox(optionUIClass.cbY,e=1,en=1)
			cmds.checkBox(optionUIClass.cbZ,e=1,en=1)
			#cmds.rowColumnLayout(optionUIClass.setLayout,e=1,en=1)
	
	@classmethod 
	def cb_YZ_command(cls):
		y = cmds.checkBox(optionUIClass.cbY,q=1,v=1)
		if cmds.checkBox(optionUIClass.cbZ,q=1,v=1) == 1:
			z = 2
		else:
			z = 0
		optionUIClass.YZ_value = y + z
		return 
	@classmethod
	def cb_M_command(cls):
		optionUIClass.Mirror_value = cmds.checkBox(optionUIClass.cbM,q=1,v=1)
	
	@classmethod 
	def button1_command(cls):
		if optionUIClass.cb_value:
			optionJointClass.option_createShiJoint()
		else:
			optionJointClass.option_createYiJoints()

#-------------------------
#
# option_setUI
#
#-------------------------

def option_setUI_cb1():
		cmds.checkBox("option_setUI_cb2",e=1,v=0)
		if not cmds.checkBox("option_setUI_cb1",q=1,v=1):
			cmds.checkBox("option_setUI_cb2",e=1,v=1)
def option_setUI_cb2():
		cmds.checkBox("option_setUI_cb1",e=1,v=0)
		if not cmds.checkBox("option_setUI_cb2",q=1,v=1):
			cmds.checkBox("option_setUI_cb1",e=1,v=1)



def option_setUI(winName = "option_setWin"):
	if cmds.window(winName,ex=1):
		cmds.deleteUI(winName)

	cmds.window(winName,t="十字骨骼设置")
	cmds.columnLayout(adj=1)
	cmds.text(l="设置跟随  (+/-  ,  + ,  -)",w=20,h=30)
	cmds.separator()
	cmds.rowColumnLayout(nbg=1,nc=7,h=40)
	cmds.text(l="",w=15)
	cmds.button(h=30,w=50,l="跟随 +/-",c = 'option_setFollow(f=0)')
	cmds.text(l="",w=10)
	cmds.button(h=30,w=50,l="跟随  +", c = 'option_setFollow(f=1)')
	cmds.text(l="",w=10)
	cmds.button(h=30,w=50,l="跟随  -", c = 'option_setFollow(f=2)')
	cmds.text(l="",w=10)
	cmds.setParent("..")
	cmds.separator()
	cmds.text(l="查看骨骼某轴向上，选择某轴",w=10)
	cmds.rowColumnLayout(nbg=1,nc=4,)
	cmds.text(l="",w=50)
	cmds.checkBox("option_setUI_cb1",v=1,w=30,h=20,label='Y', cc = 'option_setUI_cb1()')
	cmds.text(l="",w=30)
	cmds.checkBox("option_setUI_cb2",v=0,w=30,h=20,label='Z', cc = 'option_setUI_cb2()')
	cmds.setParent("..")
	cmds.text(l="",h=10)
	cmds.button(h=40,w=50,l="纠正关联",c = 'Option_correctLine()')
	cmds.text(l="",h=5)
	cmds.separator()
	cmds.text(l="",h=5)
	cmds.button(h=40,w=50,l="镜像属性",c = 'Option_MirrorLRAttr()')

	cmds.showWindow(winName)






#-------------------------
#
# createShiJoint
#
#-------------------------
def option_lock(obj,l=1,attr=None):
	if type(attr) != list:
		return cmds.error("attr not list")
	attrName = [(obj+"."+a) for a in attr]
	if l==1:
		allAttr = pm.ls(obj)[0].listAttr(l=1)
		for a in allAttr:
			if str(a) in attrName:
				continue
			pm.setAttr(a,l=0)
	if l==0:
		allAttr = pm.ls(obj)[0].listAttr(k=1)
		for a in allAttr:
			if str(a) in attrName:
				continue
			pm.setAttr(a,l=1)

def option_createTwoJoint(name,p=None):
	if type(p) != list:
		return cmds.error("p not list")

	cmds.select(cl=1)
	if len(p) == 1:
		jointName = name +"_joint1"
		cmds.joint(n=jointName,p=p[0])
		cmds.select(cl=1)
		return jointName
	elif len(p) == 2:
		jointName1 = name +"_joint1"
		jointName2 = name +"_joint2"
		cmds.joint(n=jointName1,p=p[0])
		cmds.joint(n=jointName2,p=p[1])
		cmds.joint(jointName1,e=1,zso=1,oj="xyz",sao="yup")
		cmds.joint(jointName2,e=1,oj="none",ch=1,zso=1)
		cmds.select(cl=1)
		jointName =[jointName1,jointName2]

		return jointName
	else:
		cmds.error("must one or two list")

def option_createJoint(obj):
	firstJointName = []
	nextJointName = []
	lastJointName =[]
	
	objName = obj + "_Option"
	#ro = pm.xform(obj,q=1,ws=1,ro=1)
	#tr = pm.xform(obj,q=1,ws=1,t=1)

	five_p =[[0,0,0],[0,1,0],[0,0,1],[0,-1,0],[0,0,-1]]

	for v in range(1,101):
		if cmds.objExists(objName+"First"+str(v)+"_joint1") == 0:
			na1 = objName+"First"+str(v)
			break
	for a in ["A","B","C","D","E","F","G","H","L","M","N","O","P","Q","R","S","T","U","I","Y"]:
			if cmds.objExists(objName+a+"1_joint1") == 0 or cmds.objExists(objName+a+"2_joint1") == 0 or cmds.objExists(objName+a+"3_joint1") == 0 or cmds.objExists(objName+a+"4_joint1") == 0:
				na2 = objName+a
				break
	for i in range(0,5):
		if i == 0:
			C_jointName = option_createTwoJoint(name= na1,p=[five_p[0],])
			firstJointName.append(C_jointName)
		else:
			N_jointName = option_createTwoJoint(name= na2+str(i),p=[five_p[0],five_p[i]])
			cmds.parent(N_jointName[0],C_jointName)
			cmds.select(cl=1)

			if i == 2 :
				cmds.setAttr((N_jointName[0]+".rotateX"), -90)
			if i == 4 :
				cmds.setAttr((N_jointName[0]+".rotateX"), -90)

			nextJointName.append(N_jointName[0])
			lastJointName.append(N_jointName[1])

	#pm.xform(C_jointName,ro=ro)
	#pm.xform(C_jointName,t = tr)
	#cmds.select(C_jointName)
	#mel.eval("channelBoxCommand -freezeRotate;")
	delp = cmds.parentConstraint(obj,C_jointName,weight=1)
	cmds.delete(delp)

	cmds.select(C_jointName)
	mel.eval("channelBoxCommand -freezeRotate;")

	par_name = cmds.listRelatives(obj,p=1)
	if par_name != None:
		cmds.parentConstraint(par_name[0],C_jointName,mo=1,weight=1)
	cmds.select(cl=1)
	for i in range(0,len(nextJointName)):
		option_lock(lastJointName[i],l=0,attr=["translateX",])
		option_lock(nextJointName[i],l=0,attr=["rotateZ",])
		
	allJointName =[firstJointName,nextJointName,lastJointName]

	if cmds.objExists("option_joints_G"):
		cmds.parent(firstJointName,"option_joints_G")
	else:
		cmds.group(n="option_joints_G",em=1)
		cmds.parent(firstJointName,"option_joints_G")

	return allJointName

def option_mirrorJoint(obj = None):

	newSlJoint = []
	if obj == None:
		slJoint = optionJointClass.selectJoint
	else:
		slJoint = obj
	if slJoint == None:
		cmds.error("not slect to joint")

	allJoint = cmds.ls(type="joint")
	allJointPosition =[[round(x,4) for x in v ] for v in [cmds.xform(x,q=1,ws=1,t=1) for x in allJoint]]
	jointPosition ={}
	for x,y in zip(allJoint,allJointPosition):
		jointPosition[x] = y
	
	for j in slJoint:

		allR =list(set([j.replace(x,y) for x,y in zip(["L","Left","l","left"],["R","Right","r","right"])]))
		R = [allR[i] for i in range(len(allR)) if allR[i] !=str(j)]
		joint_R = []
		if R !=[]:
			[joint_R.append(r) for r in [x for x in R if pm.objExists(x)]]
		if joint_R != []:
			try:
				cmds.select(joint_R[0])
			except:
				cmds.error("存在 two joint name : %s " % joint_R[0])
			cmds.select(cl=1)

		else:
			l_position = jointPosition[j]
			r_position =[]
			for i in range(len(l_position)):
				if i==0 :
					r_position.append(l_position[i]*-1.0)
				else:
					r_position.append(l_position[i])
			[joint_R.append(r) for r in [k for k in jointPosition.keys() if r_position == jointPosition[k]]]
		
		get_R = list(set(joint_R))
		if len(get_R) !=1:
			cmds.error("存在 %i joint name : %s " % (len(get_R),get_R))
		newSlJoint.append(get_R[0])

	return newSlJoint

def option_addAttr(obj,attr,at="double",dv=1):
	objAttr = obj+"."+attr
	cmds.addAttr(obj,k=1,ln=attr,at=at,dv=dv)
	cmds.setAttr(objAttr,k=0,cb=1)
	return objAttr

#-------------------------
#
# createFollowLine to ShiJoint
#
#-------------------------
def option_createMul(name,inputAttr_1,inputAttr_2,xz="X"):
	
	mulName = cmds.createNode("multiplyDivide",n=(name +"_mul"))
	cmds.connectAttr(inputAttr_1,mulName+".input1"+xz)
	cmds.connectAttr(inputAttr_2,mulName+".input2"+xz)
	return mulName

def option_createPlus(name,inputAttr_1,inputAttr_2,outputAttr,xz="X"):
	
	plusName = cmds.createNode("plusMinusAverage",n=(name +"_plus"))
	cmds.connectAttr(inputAttr_1,plusName+".input3D[0].input3D"+xz.lower())
	cmds.setAttr(plusName+".input3D[1].input3D"+xz.lower(),inputAttr_2)
	cmds.connectAttr(plusName+".output3D"+xz.lower(),outputAttr)
	
	return plusName

def option_createFollow(f,n,l,yz=None):
	if type(yz) == list:
		y = yz[0]
		z = yz[1]
	else:
		y = yz
		z = yz
	
	for i in range(4):
		option_addAttr(n[i],"slide")
		
		if i == 0 or i == 2 :
			option_addAttr(l[i],"slide",dv=-0.01)
			mul = option_createMul(name = l[i],inputAttr_1= f+".r"+z,inputAttr_2 = l[i]+".slide",xz="X")
			if i == 0:
				plu1 = option_createPlus(name = l[i] ,inputAttr_1 = mul+".outputX" ,inputAttr_2 = cmds.getAttr(l[i]+".tx"),outputAttr = l[i]+".tx",xz="X")
			else:
				cmds.connectAttr(mul+".outputX",plu1+".input3D[0].input3Dz")
				cmds.setAttr(plu1+".input3D[1].input3Dz",cmds.getAttr(l[i]+".tx"))
				cmds.connectAttr(plu1+".output3Dz",l[i]+".tx")
			if z == "z":
				cmds.connectAttr(f+".r"+z,mul+".input1Z")
				cmds.connectAttr(n[i]+".slide",mul+".input2Z")
				cmds.connectAttr(mul+".outputZ",n[i]+".rz")
			else:
				cmds.deleteAttr(n[i],attribute="slide")
		if i == 1 or i == 3 :
			option_addAttr(l[i],"slide",dv=0.01)
			mul = option_createMul(name = l[i],inputAttr_1= f+".r"+y,inputAttr_2 = l[i]+".slide",xz="X")
			if i == 1:
				plu2 = option_createPlus(name = l[i] ,inputAttr_1 = mul+".outputX" ,inputAttr_2 = cmds.getAttr(l[i]+".tx"),outputAttr = l[i]+".tx",xz="X")
			else:
				cmds.connectAttr(mul+".outputX",plu2+".input3D[0].input3Dz")
				cmds.setAttr(plu2+".input3D[1].input3Dz",cmds.getAttr(l[i]+".tx"))
				cmds.connectAttr(plu2+".output3Dz",l[i]+".tx")
			if y == "y":
				cmds.connectAttr(f+".r"+y,mul+".input1Z")
				cmds.connectAttr(n[i]+".slide",mul+".input2Z")
				cmds.connectAttr(mul+".outputZ",n[i]+".rz")
			else:
				cmds.deleteAttr(n[i],attribute="slide")
	cmds.select(cl=1)

def option_createFollowLine(obj,p=None):
	if type(p) != list:
		return cmds.error("inputAttr not list")
	value = optionUIClass.YZ_value
	if value == 0:
		cmds.error("select to UI Y or Z")
	if value == 1:
		option_createFollow(f = obj,n = p[1],l = p[2],yz="y")
	
	if value == 2:
		option_createFollow(f = obj,n = p[1],l = p[2],yz="z")
	
	if value == 3:
		option_createFollow(f = obj,n = p[1],l = p[2],yz=["y","z"])
	return 

#-------------------------
#
# createFollowLine to YiJoint
#
#-------------------------
def option_getWorldPosition(obj):
	p = cmds.xform(obj,q=1,ws=1,t=1)
	return p

def option_createJoint_y(poistion1,poistion2,name):

	j1 = cmds.joint(n = name + "_MusJoint1",p=poistion1)
	j2 = cmds.joint(n = name + "_MusJoint2",p=poistion2)
	cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
	cmds.joint(j2,e=1,oj="none",ch=1,zso=1)
	cmds.select(cl=1)

	return [j1,j2]

def option_par(obj1,obj2):

	p = cmds.parentConstraint(obj1,obj2,weight=1)
	cmds.delete(p)

def option_createCircle(name):

	ctrl = cmds.circle(n=name+"_MusCtrl",nr=(1,0,0))
	cmds.setAttr(ctrl[0]+".overrideEnabled", 1)
	cmds.setAttr(ctrl[0]+".overrideColor", 17)
	cmds.delete(ctrl[1])
	attr = ["rx","ry","rz","sx","sy","sz","v"]
	[cmds.setAttr(ctrl[0]+ "."+a ,lock=True ,keyable=False,channelBox=False)  for a in attr]

	c = cmds.group(n=ctrl[0]+"_C",em=1)
	g = cmds.group(n=ctrl[0]+"_G",em=1)

	cmds.parent(ctrl[0],c)
	cmds.parent(c,g)
	
	return [ctrl[0],g]

def option_createYiJoint(obj):

	cmds.select(cl=1)
	j1 = cmds.joint(p=(0,0,0))
	j2 = cmds.joint(p=(2,0,0))
	cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
	option_par(obj,j1)
	cmds.select(cl=1)

	return j1

def option_addDisBet(name,i,input1,input2):

	db = cmds.createNode("distanceBetween",n=name+"_disBet"+str(i),)

	cmds.connectAttr(input1+".translate",db+".point1")
	cmds.connectAttr(input2+".translate",db+".point2")

	return db

def getScaleValue(obj1,obj2,r="p"):

	p1 = cmds.xform(obj1,q=1,ws=1,t=1)
	p2 = cmds.xform(obj2,q=1,ws=1,t=1)

	cmds.select(cl=1)
	j1 = cmds.joint(p=p1)
	j2 = cmds.joint(p=p2)
	cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
	cmds.select(cl=1)

	t = cmds.getAttr(j2+".tx")/2.50
	g1 = cmds.group(em=1)
	g2 = cmds.group(em=1)
	cmds.parent(g1,g2)

	cmds.delete(cmds.parentConstraint(j1,g2,weight=1))

	cmds.setAttr(g1+".tx",t)
	p = cmds.xform(g1,q=1,ws=1,t=1)

	cmds.delete((j1,g2))

	if r == "p":
		return p
	if r == "t":
		return t


def option_doItYiJointLine(name,aimObj,jnt1,jnt2):

	p1 = option_getWorldPosition(jnt1)
	p2 = option_getWorldPosition(jnt2)
	j = option_createJoint_y(p1,p2,name)

	"""
	option_par(jnt1,j[0])
	cmds.makeIdentity(j[0],apply=True,t=0,r=1,s=0,n=0,pn=1)
	"""
	ikHandle = cmds.ikHandle(n=name + "_ikHandle1",sj=j[0],ee=j[1])[0]
	ctrl = option_createCircle(name)

	option_par(j[1],ctrl[1])
	cmds.parent(ikHandle,ctrl[0])
	cmds.setAttr(ikHandle+".v",0)

	
	aimG = [cmds.group(n= (name + "_scaleAim_" + x + y),em=1)  for x in ["A","B"] for y in ["1","2"] ]
	aimS = cmds.group(n= (name + "_scaleAim_G"),em=1)
	cmds.parent(aimG,aimS)

	option_par(j[0],aimG[0])
	option_par(j[1],aimG[1])
	option_par(j[0],aimG[2])
	option_par(j[1],aimG[3])


	g1 = cmds.group(n= name + "_YiIK_G",em=1)
	g2 = cmds.group(n= name + "_YiIK_Ro",em=1)
	g3 = cmds.group(n= name + "_AimUp",em=1)
	cmds.parent((g2,g3),g1)
	option_par(j[0],g1)
	y = getScaleValue(j[0],j[1],"t")
	cmds.setAttr(g3+".ty",y)

	cmds.parent(ctrl[1],g2)
	cmds.parent(aimS,g1)
	cmds.parent(j[0],g1)

	g4 = aimObj + "_del_Aim"
	g5 = aimObj + "_optionAim"
	if cmds.objExists(g5) == False:

		cmds.group(n= g4,em=1)
		cmds.group(n= g5,em=1)

		cmds.parent(g5,g4)
		option_par(aimObj,g4)
		if cmds.getAttr(aimObj+".tx") > 0:
			cmds.setAttr(g5+".tx",0.5)
		if cmds.getAttr(aimObj+".tx") < 0:
			cmds.setAttr(g5+".tx",-0.5)

		cmds.parent(g5,w=1)
		down = cmds.listRelatives(aimObj,c=1)
		if down != None:
			t = getScaleValue(aimObj,down[0])
			[cmds.setAttr(g5+".t"+x,y) for x,y in zip(["x","y","z"],t) ]

		cmds.parentConstraint(aimObj,g5,mo=1,weight=1)

	if cmds.objExists("optionAim_G") == False:
		cmds.group(n="optionAim_G",em=1)

	l = cmds.listRelatives("optionAim_G",c=1)
	if l == None:
		l = []

	if g5 not in l:
		cmds.parent(g5,"optionAim_G")

	if cmds.objExists(g4):
		cmds.delete(g4)

	cmds.aimConstraint(g5,g2,mo=1,weight=1,aimVector=(1,0,0) ,upVector=(0,1,0),worldUpType="object",worldUpObject=g3)
	cmds.parentConstraint(ctrl[0],aimG[1],mo=1,weight=1)
	cmds.parentConstraint(g5,aimG[3],mo=1,weight=1)

	db1 = option_addDisBet(name,i=1,input1=aimG[0],input2 = aimG[1])
	cmds.connectAttr(db1+".distance",j[1]+".tx")
	
	db2 = option_addDisBet(name,i=2,input1=aimG[2],input2 = aimG[3])

	mulName = cmds.createNode("multiplyDivide",n=(name +"_mul"))
	cmds.connectAttr(db2+".distance",mulName+".input1X")
	cmds.setAttr(mulName+".input2X",cmds.getAttr(mulName+".input1X"))
	cmds.setAttr(mulName+".operation",2)

	cmds.connectAttr(mulName+".outputX",g2+".sx")

	if not cmds.objExists("optionYiIK_G"):
		cmds.group(n="optionYiIK_G",em=1)
		cmds.parent(str(g1),"optionYiIK_G")
	else:
		cmds.parent(str(g1),"optionYiIK_G")


	
	return g1

#-------------------------
#
# optionJointClass (shi and yi joint)
#
#-------------------------

class optionJointClass(object):

	def __init__(self):
		self.allJoint = None
		self.selectJoint = None
		self.aimObj = None
		self.rightJoint = None
		self.locationJoint = None
	
	@classmethod
	def option_allSelct(self):
		self.rightJoint = []
		self.locationJoint = {}
		slObj = cmds.ls(sl=1)
		if slObj !=[]:
			self.selectJoint = slObj
			return slObj
		else:
			cmds.error("must select to object")

	def option_selectJoint(self):
		self.selectJoint = optionJointClass.option_allSelct()

	@classmethod
	def option_LocatorJoint(self):
		sl = pm.ls(sl=1)
		if optionUIClass.cb_value == True:
			if len(sl) == 2:
				optionJointClass.locationJoint[str(sl[1])] = str(sl[0])
				if sl != []:
					par = list(set([str(x) for x in sl[1].inputs()]))[0]
					if par != []:
						cmds.delete(par)
					pm.parentConstraint(sl[0],sl[1],weight=1)
					cmds.select(cl=1)
					print ("////重新定位完成"+"\n"),
			else:
				cmds.error("选择单个固定骨骼，再选择单个添加骨骼")
		if optionUIClass.cb_value == False:
			if len(sl) == 2:
				option_par(str(sl[0]),str(sl[1]))
			else:
				cmds.error("选择单个固定骨骼，再选择单个添加骨骼")

	@classmethod
	def option_createShiJoint(self,obj=None):
		jointName = []
		if obj == None:
			obj = optionJointClass.option_allSelct()
		for o in obj:
			threeJointName =option_createJoint(o)
			jointName.append(threeJointName)
		self.allJoint = jointName
		print ("////创建辅助骨骼成功"+"\n"),
		return jointName

	@classmethod 
	def option_createYiJoints(self,obj=None):
		jointName = []
		obj = optionJointClass.option_allSelct()
		if len(obj) > 1:
			self.aimObj = obj[0]
			for o in range(1,len(obj)):
				yiJointName = option_createYiJoint(obj[o])
				jointName.append(yiJointName)
			self.allJoint = jointName
		else:
			cmds.error("选择目标骨骼，再选择位置物体")
		print ("////创建辅助骨骼成功"+"\n"),
		return jointName

	@classmethod
	def optionShiJointLine(self,M=None,obj=None):

		if M == None:
			m = optionUIClass.Mirror_value
		else :
			m = M

		if obj != None:
			self.selectJoint = obj
			newallJoint = []
			for x in self.allJoint:
				for y in list(set(obj)):
					if y in str(x[0][0]):
						newallJoint.append(x)

		if m:
			newJoint = option_mirrorJoint(obj)
			self.rightJoint = newJoint

			if obj == None:
				[self.selectJoint.append(n) for n in newJoint]
			else:
				self.selectJoint = obj + newJoint

			for i in range(len(newJoint)):
				allJointName = option_createJoint(newJoint[i])

				if obj == None:
					l = self.allJoint[i][2]
					l_0 = self.allJoint[i][0]
					l_1 = self.allJoint[i][1]
				else:
					l = newallJoint[i][2]
					l_0 = newallJoint[i][0]
					l_1 = newallJoint[i][1]

				all_l = l_0 + l_1 + l

				r = allJointName[2]
				r_0 = allJointName[0]
				r_1 = allJointName[1]
				all_r = r_0 + r_1 + r

				[ pm.setAttr(x+".radi",float(pm.getAttr(y+".radi"))) for x,y in zip(all_r,all_l)]
				
				pm.setAttr(r[0]+".tx",float(pm.getAttr(l[2]+".tx")))
				pm.setAttr(r[1]+".tx",float(pm.getAttr(l[3]+".tx")))
				pm.setAttr(r[2]+".tx",float(pm.getAttr(l[0]+".tx")))
				pm.setAttr(r[3]+".tx",float(pm.getAttr(l[1]+".tx")))
				self.allJoint.append(allJointName)

				if self.locationJoint != {}:
					
					if obj == None:
						s = str(self.allJoint[i][0][0])
					else:
						s = str(newallJoint[i][0][0])

					if s in self.locationJoint.keys():
						Lp = self.locationJoint[s]
						Rp = option_mirrorJoint([Lp,])[0]
						
						try:
							par = list(set([str(x) for x in pm.ls(allJointName[0])[0].inputs()]))[0]
							if par != []:
								cmds.delete(par)
							pm.parentConstraint(Rp,allJointName[0],weight=1)
						except:
							cmds.error("Not Mirror Parent joint")

				if obj != None:
						option_createFollowLine(self.rightJoint[i],allJointName)

		if self.selectJoint == None or self.allJoint ==None:
			return cmds.error("not create to option of the Joint")
		if optionUIClass.YZ_value == 0:
				cmds.error("select to Y or Z")

		if obj == None:
			for s,a in zip(self.selectJoint,self.allJoint):
				option_createFollowLine(s,a)
			print "------关联骨骼成功-------\n",
		else:
			for x,y in zip(self.selectJoint,newallJoint):
				option_createFollowLine(x,y)
			print "------关联骨骼成功-------\n",

		if self.rightJoint != []:
			[self.selectJoint.remove(self.rightJoint[i]) for i in range(len(self.rightJoint)) if self.rightJoint[i] in self.selectJoint]
	
	@classmethod
	def optionJointLine(self):

		if optionUIClass.cb_value :

			optionJointClass.optionShiJointLine()

		else:
			if optionUIClass.Mirror_value:
				newJoint = option_mirrorJoint(obj = [self.aimObj,])
				if newJoint != []:
					allJnt_r = []
					for a in self.allJoint:
						jnt = cmds.mirrorJoint(a,mirrorYZ=1,mirrorBehavior=1,searchReplace =("Left","Right"))
						jnt1 = cmds.listRelatives(a,c=1)[0]

						Mir1 = a + "_Mirror1"
						Mir2 = a + "_Mirror2"

						cmds.rename(jnt[1],Mir2)
						cmds.rename(jnt[0],Mir1)
						allJnt_r.append(Mir1)
					optionJointClass.optionJointYiLine(aim=newJoint[0],allJnt=allJnt_r)

			optionJointClass.optionJointYiLine(aim=self.aimObj,allJnt=self.allJoint)

		print ("////Add OptionJoint ok -----"+"\n"),

	@classmethod
	def optionJointYiLine(self,aim,allJnt):

		cmds.select(cl=1)
		aimObj = aim

		if len(self.allJoint) == 1:
			if cmds.objExists(aimObj + "_Option_YiIK_G") == True:
				name = None
			else:
				name = aimObj + "_Option"

		if len(self.allJoint) > 1 or name == None :
			for i in range(1,100):
				if cmds.objExists(aimObj + "_Option" + str(i)+"_YiIK_G") == False:
					ii = i
					break
				else:
					continue

		all = allJnt
		for j in all:

			if len(self.allJoint) > 1 or cmds.objExists(aimObj + "_Option_YiIK_G") == True:
				name = aimObj + "_Option" + str(ii)
				ii=ii+1

			j1 = j
			j2 = cmds.listRelatives(j1,c=1)[0]
			option_doItYiJointLine(name,aimObj,j1,j2)
			cmds.delete(j)

def option_setFollow(f=0,obj=None):
	if obj == None:
		sl = pm.ls(sl=1)
	else:
		sl = pm.ls(obj)
	for s in sl :
		a = s.listAttr(u=1,k=1)[0]
		r = a.split(".")[1].split("te")
		if len(r)!= 2:
			cmds.error("please select to option of the Joint")
		ar = r[0]+"tion"+r[1]
		
		e = "enable"+ar[0].capitalize()+ar[1:-1]+r[1]
		get = s.getAttr(a.split(".")[1])
		if f ==0:
			exec('pm.transformLimits(s,%s=(-1,1),%s=(0,0))' % (ar,e))
			print("/////set ok ....."+"\n"),
		if f == 1:
			exec('pm.transformLimits(s,%s=(%f,%f),%s=(0,1))' % (ar,get,get,e))
			print("/////set ok ....."+"\n"),
		if f == 2:
			exec('pm.transformLimits(s,%s=(%f,%f),%s=(1,0))' % (ar,get,get,e))
			print("/////set ok ....."+"\n"),



#-------------------------
#
# add ADV option joint
#
#-------------------------
def advSetTx(jointList,value,AB="A",attr = "tx"):
	j = [s+"_Option"+ss+"_joint2" for s in jointList for ss in [AB+"1",AB+"2",AB+"3",AB+"4"]]
	[cmds.setAttr(x+"."+attr,value) for x in j]

def advSetTxToOne(jnt,value,AB="A",attr = "tx"):
	j = [jnt+"_Option"+ss+"_joint2" for ss in [AB+"1",AB+"2",AB+"3",AB+"4"]]
	[cmds.setAttr(x+"."+attr,value) for x in j]

def doItAddAdvOptionJoint(*args):

	if cmds.objExists("Root_M") == 1:

		n = cmds.createNode("distanceBetween")
		newG = cmds.group(em=1)
		cmds.parentConstraint("Root_M",newG)
		cmds.connectAttr(newG+".translate",n+".point2")
		flo = cmds.getAttr(n+".distance")
		num = flo / 1.0137173930603345
		cmds.delete(n,newG)

	else:
		num = 1

	advSlider = cmds.ls("*Slide*")

	try:
		ss = cmds.listRelatives("SlideSystem",c=1)
	except:
		ss = []

	try:
		ds = cmds.listRelatives("DeformationSystem",c=1)
	except:
		ds = []

	try:
		Slider = [ s for s in advSlider if s in (ss + ds) ]
	except:
		Slider = []
	
	if Slider != []:
		bool_T = cmds.confirmDialog(t="ADV Slide joint",m="是否删去ADV生成的辅助骨骼?",b=("Yes","No"))
		if bool_T == "Yes":
			cmds.delete(advSlider)

	advLeg_l = ["Toes_L","Ankle_L","Knee_L","Hip_L"]
	advLeg_r = [s.replace("L","R") for s in advLeg_l]
	advSpine = ["Root_M","Spine1_M","Spine2_M","Spine3_M","Neck_M","Head_M"]
	advShoulder_l = ["Shoulder_L","Elbow_L","Wrist_L"]
	advShoulder_r = [s.replace("L","R") for s in advShoulder_l]

	advFinger_five = ["Thumb","Index","Middle","Ring","Pinky"]
	advFinger_l = [s+"Finger"+str(i)+"_L" for s in advFinger_five for i in [1,2,3]]
	advFinger_r = [s.replace("L","R") for s in advFinger_l]

	newB = ["Elbow_L","Knee_L"]
	adv = optionJointClass()
	cmds.select((advLeg_l+advShoulder_l+advSpine+advFinger_l))
	adv.option_allSelct()
	adv.option_selectJoint()
	[ adv.selectJoint.append(x) for x in newB ]

	allJoints = adv.option_createShiJoint(adv.selectJoint)

	cmds.select("ShoulderPart2_L","Elbow_L_OptionFirst2_joint1")
	adv.option_LocatorJoint()
	cmds.select("HipPart2_L","Knee_L_OptionFirst2_joint1")
	adv.option_LocatorJoint()
	cmds.select(cl=1)
	
	f = [s[0][0] for s in allJoints]
	A = [s[i][ii] for s in allJoints for i in range(1,3) for ii in range(0,4)]
	joints = f + A
	
	[cmds.setAttr(j+".radi",0.5*num) for j in joints ]
	
	advSetTx(advFinger_l,0.02*num)
	
	[ advSetTxToOne(advShoulder_l[i],v*num) for i,v in  zip(range(0,3),[0.08,0.05,0.04]) ]
	[ advSetTxToOne(advLeg_l[i],v*num) for i,v in  zip(range(0,4),[0.05,0.06,0.1,0.12]) ]

	[ advSetTxToOne(newB[i],v*num,AB="B") for i,v in  zip(range(0,2),[0.06,0.11]) ]

	for s in advSpine:
		sof = s + "_OptionFirst1_joint1"
		sofp = sof + "_parentConstraint1"
		parObj = cmds.listConnections(sofp + ".target[0].targetParentMatrix")[0]

		cmds.delete(sofp)
		cmds.setAttr(sof+".rz",90)

		cmds.parentConstraint(parObj,sof,mo=1,weight=1)

	[ advSetTxToOne(advSpine[i],v*num) for i,v in  zip(range(0,6),[0.15,0.15,0.15,0.15,0.08,0.08]) ]

	[ cmds.setAttr(x+".tx",cmds.getAttr(x+".tx")*0.5) for x in ["Knee_L_OptionA2_joint2","Knee_L_OptionB2_joint2","Hip_L_OptionA2_joint2"]]

	getNum.num = num
	opcj = Option_CreateChestJoint(num)
	yi = Option_CreateADVYIoint(num)
	print "------ADV辅助骨骼创建完成-----------",



def advSetSlide(jointList,value,AB="A",attr = "tx",st="2"):
	j = [s+"_Option"+ss+"_joint"+st for s in jointList for ss in [AB+"1",AB+"2",AB+"3",AB+"4"]]
	for x in j:
		i = cmds.getAttr(x+"."+attr)
		cmds.setAttr(x+"."+attr,value*i) 

def advSetSlideToOne(x,value,attr = "slide"):
	i = cmds.getAttr(x+"."+attr)
	cmds.setAttr(x+"."+attr,value*i)

def advSetFollow(jointList,AB="A",st="2",f=0):
	j = [s+"_Option"+ss+"_joint"+st for s in jointList for ss in [AB+"1",AB+"2",AB+"3",AB+"4"]]
	option_setFollow(f,j)

def advSetAttr(l,r,sli,e,attr):
	if cmds.objExists(r):
		cmds.setAttr(r+"."+sli,cmds.getAttr(l+"."+sli))

		exec('tf = cmds.transformLimits('+'\"' + l + '\"' + ',q=1,'+ e + '=1)')
		exec('cmds.transformLimits('+'\"' + r + '\"' + ','+ e + '='+ str(tf) +')')

		exec('tn = cmds.transformLimits('+'\"' + l + '\"' + ',q=1,'+ attr + '=1)')
		exec('cmds.transformLimits('+'\"' + r + '\"' + ','+ attr + '='+ str(tn) +')')

	else:
		cmds.error(r + " not exists.......")

def advSetMirrorAttr(obj,AB,i,sli,e,attr):
	l = [ (obj + "_Option" + AB + str(x) + "_joint" + str(i))  for x in [1,2,3,4] ]
	r = [ (obj.replace("L","R") + "_Option" + AB + str(x) + "_joint" + str(i))  for x in [3,4,1,2] ]
	[advSetAttr(x,y,sli,e,attr)  for x,y in zip(l,r)]

def advSetNewRo(obj,newRo,cb=1):

	m =  cmds.listConnections(obj, type = "multiplyDivide")[0]
	up_j =  cmds.listConnections(obj, type = "joint")[0]

	unit = cmds.listConnections(m, type = "unitConversion")
	j = cmds.listConnections(unit[0], type = "joint")[0]

	[mel.eval("CBdeleteConnection "+ "\"" + m + ".input1" + x +"\";") for x in ["X","Z"] ]
	[cmds.connectAttr((j+"."+newRo),(m+".input1"+x)) for x in ["X","Z"] ]

	a = cmds.listAttr(up_j,u=1,k=1)[0]
	if cb == 1:
		mel.eval("CBdeleteConnection "+ "\"" + up_j + "." + a +"\";")

def advGetName(obj,AB,num,i):

	n = obj + "_Option"+AB + str(num) + "_joint" + str(i)

	return n 

def advSetSpineRo(obj,newRo,cb=0):

	j = [advGetName(obj,"A",y,z) for y in [2,4] for z in [1,2]]

	[ advSetNewRo(x,newRo,cb) for x in j ]



def doItAddAdvOptionJointLine(*args):
	s_L = [ x for x in optionJointClass.selectJoint if "_L" in x ]
	s_M = [ x for x in optionJointClass.selectJoint if "_M" in x ]

	optionJointClass.optionShiJointLine(M=True,obj=s_L)
	optionJointClass.optionShiJointLine(M=False,obj=s_M)

	if cmds.objExists("Main"):
		cmds.parent("option_joints_G","Main")
		cmds.select(cl=1)

	advLeg_l = ["Toes_L","Ankle_L","Knee_L","Hip_L"]
	advSpine = ["Root_M","Spine1_M","Spine2_M","Spine3_M","Neck_M","Head_M"]
	advShoulder_l = ["Shoulder_L","Elbow_L","Wrist_L"]

	advFinger_five = ["Thumb","Index","Middle","Ring","Pinky"]
	advFinger_l = [s+"Finger"+str(i)+"_L" for s in advFinger_five for i in [1,2,3]]

	advSetSlide(advFinger_l,0.02,"A","slide",st="2")
	advSetSlide((advLeg_l + advSpine + advShoulder_l),0.07,"A","slide",st="2")
	advSetSlide(["Knee_L","Elbow_L"],0.07,"B","slide",st="2")

	advSetSlide((advLeg_l + advSpine + advShoulder_l + advFinger_l),0.5,"A","slide",st="1")
	advSetSlide(["Knee_L","Elbow_L"],0.15,"B","slide",st="1")

	advSetSlide(["Toes_L","Ankle_L","Hip_L","Elbow_L","Wrist_L"],-1,"A","slide",st="2")
	advSetSlide(["Elbow_L"],-1,"B","slide",st="2")

	[cmds.setAttr(x+".slide",0.75) for x in ["Ankle_L_OptionA1_joint1","Ankle_L_OptionA3_joint1"]]
	[cmds.setAttr(x+".slide",0.25) for x in ["Shoulder_L_OptionA1_joint1","Shoulder_L_OptionA3_joint1"]]

	[advSetSlideToOne(x,-1,"slide") for x in ["Toes_L_OptionA1_joint2","Toes_L_OptionA2_joint2","Ankle_L_OptionA1_joint2","Ankle_L_OptionA2_joint2","Hip_L_OptionA1_joint2","Shoulder_L_OptionA3_joint2","Wrist_L_OptionA2_joint2","Wrist_L_OptionA1_joint2"]]
	
	unFollow  = ["Toes_L","Ankle_L","Hip_L","Shoulder_L","Wrist_L"] + advFinger_l
	advSetFollow(unFollow,"A","2",2)

	[advSetMirrorAttr(x,"A",1,"slide","erz","rz") for x in advLeg_l + advShoulder_l + advFinger_l]
	[advSetMirrorAttr(x,"A",2,"slide","etx","tx") for x in advLeg_l + advShoulder_l + advFinger_l]

	[advSetMirrorAttr(x,"B",1,"slide","erz","rz") for x in ["Knee_L","Elbow_L"] ]
	[advSetMirrorAttr(x,"B",2,"slide","etx","tx") for x in ["Knee_L","Elbow_L"] ]


	roL = ["Knee_L_OptionA2_joint2","Knee_L_OptionA4_joint2","Knee_L_OptionB2_joint2","Knee_L_OptionB4_joint2","Elbow_L_OptionB4_joint2","Elbow_L_OptionB2_joint2","Elbow_L_OptionA4_joint2","Elbow_L_OptionA2_joint2" ]
	roR = [x.replace("L","R") for x in roL]

	[ advSetNewRo(x,"rz") for x in  roL + roR ]
	[ advSetSlideToOne(x,-1) for x in roL + roR ]

	cmds.delete("Spine1_M_OptionFirst1_joint1_parentConstraint1")
	cmds.parentConstraint("Spine1_M","Spine1_M_OptionFirst1_joint1",mo=1,weight=1)

	[advSetSpineRo(x,"rx",cb=0) for x in advSpine]
	spine_J = [advGetName(advSpine[x],"A",y,1) for x in range(1,len(advSpine)) for y in [1,3] ]
	[ advSetSlideToOne(x,-1.5) for x in spine_J ]
	[ advSetSlideToOne(x,-1) for x in ["Spine2_M_OptionA1_joint1","Spine2_M_OptionA2_joint1","Spine2_M_OptionA3_joint1","Spine2_M_OptionA4_joint1","Neck_M_OptionA4_joint1","Neck_M_OptionA2_joint1","Head_M_OptionA4_joint1","Head_M_OptionA2_joint1"]] 
	[ advSetSlideToOne(x,0) for x in ["Root_M_OptionA4_joint1","Root_M_OptionA2_joint1","Spine1_M_OptionA1_joint1","Spine1_M_OptionA2_joint1","Spine1_M_OptionA3_joint1","Spine1_M_OptionA4_joint1","Spine3_M_OptionA1_joint1","Spine3_M_OptionA2_joint1","Spine3_M_OptionA3_joint1","Spine3_M_OptionA4_joint1","Neck_M_OptionA3_joint1","Neck_M_OptionA1_joint1","Head_M_OptionA3_joint1","Head_M_OptionA1_joint1"]] 
	[ advSetSlideToOne(x,2) for x in ["Root_M_OptionA1_joint1","Root_M_OptionA3_joint1"] ]

	if cmds.objExists("Root_M_OptionFirst1_joint1_parentConstraint1"):
		cmds.delete("Root_M_OptionFirst1_joint1_parentConstraint1")
		cmds.parentConstraint("Root_M","Root_M_OptionFirst1_joint1",mo=1,weight=1)
		rm4 = cmds.listRelatives("Root_M_OptionFirst1_joint1",c=1,type="joint")
		[cmds.setAttr(x+".slide",0.5) for x in rm4]

	advSetFollow(advSpine,"A","2",2)

	j1 = [s+"_Option"+ss+"_joint2" for s in advSpine for ss in ["A1","A4"]]
	j2 = [s+"_Option"+ss+"_joint2" for s in advSpine for ss in ["A3","A2"]]

	[ advSetSlideToOne(x,-1) for x in  j1 ]
	[ advSetSlideToOne(x,5) for x in  j1+j2 ]

	cmds.setAttr("Root_M_OptionA2_joint2.slide",-0.001)
	cmds.setAttr("Root_M_OptionA3_joint1.slide",0.5)
	cmds.setAttr("Root_M_OptionA1_joint1.slide",0.5)
	cmds.setAttr("Spine1_M_OptionA2_joint2.slide",0.001)
	cmds.setAttr("Spine3_M_OptionA3_joint1.slide",0.75)
	cmds.setAttr("Spine3_M_OptionA1_joint1.slide",0.75)
	cmds.setAttr("Spine3_M_OptionA2_joint1.slide",-0.5)
	cmds.setAttr("Spine3_M_OptionA4_joint1.slide",-0.5)
	cmds.setAttr("Head_M_OptionA2_joint2.slide",-0.0035)
	option_setFollow(f=2,obj="Head_M_OptionA2_joint2")
	option_setFollow(f=2,obj="Root_M_OptionA2_joint2")

	yi = Option_doItAdvYiLine()
	chest = Option_doItChestLine()
	Option_setCircleScale()
	cmds.select(cl=1)
	print "------ADV辅助骨骼关联完成-----------",



def Option_ListOptionJoint2():

	optionJoints = cmds.listRelatives("option_joints_G",c=1,ad=1,type="joint")
	skinJoint = [s for s in optionJoints if "_joint2" in s ]

	return skinJoint



def Option_SelectToSkinJoint():
	cmds.select(Option_ListOptionJoint2())
	if cmds.objExists("optionYiIK_G"):
		yiSikn =[x for x in cmds.listRelatives("optionYiIK_G",ad=1,type="joint") for y in ["Joint2","joint2","joint4"] if y in x]
		cmds.select(yiSikn,add=1)
	print "-----选择完成-----",


class Option_ListRightObj(object):

	optionNum = 0
	allLR = {}

	@classmethod
	def listRightObj(cls):

		lr = {}

		joint2 = Option_ListOptionJoint2()
		position = [ cmds.xform(x,q=1,t=1,ws=1) for x in joint2]
		p = [ [round(o[0],6),round(o[1],6),round(o[2],6)] for o in position ]
		for i in range(0,len(p)):

			if p[i][0] > 0:
				pos = [p[i][0]*-1.000000,p[i][1],p[i][2]]
				if pos in p :
					num = p.index(pos)
					lr[joint2[i]] = joint2[num]

		for l,r in zip(lr.keys(),lr.values()):

			if pm.ls(l)[0].listRelatives(p=1)[0].listRelatives(p=1)[0] == pm.ls(r)[0].listRelatives(p=1)[0].listRelatives(p=1)[0]:
				del lr[l]

		Option_ListRightObj.allLR = lr

def Option_MirrorLRAttr():

	if len(cmds.listRelatives("option_joints_G",c=1,type="joint")) != Option_ListRightObj.optionNum:
		Option_ListRightObj.optionNum = len(cmds.listRelatives("option_joints_G",c=1,type="joint"))
		Option_ListRightObj.listRightObj()

	lr = Option_ListRightObj.allLR

	for l,r in zip(lr.keys(),lr.values()):
		Option_MirrorAttr(l,r)

		up_l = cmds.listRelatives(l,p=1)[0]
		up_r = cmds.listRelatives(r,p=1)[0]

		Option_MirrorAttr(up_l,up_r)

	print("-----镜像属性完成-----"),


def Option_MirrorAttr(obj_l,obj_r):

	slide_l = cmds.getAttr(obj_l+".slide")
	cmds.setAttr(obj_r+".slide",slide_l)

	if "_joint2" in obj_l:
		exec('tf = cmds.transformLimits('+'\"' + obj_l + '\"' + ',q=1,etx=1)')
		exec('f1 = cmds.transformLimits('+'\"' + obj_l + '\"' + ',q=1,tx=1)')
		exec('cmds.transformLimits('+'\"' + obj_r + '\"' + ',etx='+ str(tf)+",tx=" + str(f1) +')')

	if "_joint1" in obj_l:
		exec('tn = cmds.transformLimits('+'\"' + obj_l + '\"' + ',q=1,erz=1)')
		exec('f2 = cmds.transformLimits('+'\"' + obj_l + '\"' + ',q=1,rz=1)')
		exec('cmds.transformLimits('+'\"' + obj_r + '\"' + ',erz='+ str(tn) +",rz=" + str(f2) +')')



def Option_correctLine():

	sl =cmds.ls(sl=1)
	if len(sl) == 0:
		cmds.error("////选择First辅助骨骼.......")
	for s in sl:

		j = cmds.listRelatives(s,c=1,type="joint")
		par = cmds.listRelatives(s,c=1,type="parentConstraint")[0]
		parObj = cmds.listConnections(par+".target[0].targetParentMatrix")[0]
		cmds.delete(par)

		if cmds.checkBox("option_setUI_cb1",q=1,v=1):
			cmds.setAttr(s+".rz",90)
			j1 = [x for x in j if "2_joint" in x][0]
			j2 = [x for x in j if "4_joint" in x][0]

		if cmds.checkBox("option_setUI_cb2",q=1,v=1):
			cmds.setAttr(s+".ry",-90)
			j1 = [x for x in j if "1_joint" in x][0]
			j2 = [x for x in j if "3_joint" in x][0]

		cmds.parentConstraint(parObj,s,mo=1)
		
		m1 = cmds.listConnections(cmds.listConnections(j1+".rz")[0]+".input")[0]
		m2 = cmds.listConnections(cmds.listConnections(j2+".rz")[0]+".input")[0]

		uc = [cmds.listConnections(s+"."+a)[0] for s in [m1,m2] for a in ["input1X","input1Z"]]

		for u in uc:
			p = cmds.listConnections(u+".input")[0]
			plus = cmds.listConnections(u+".input",p=1)[0]
			cmds.disconnectAttr(plus,u+".input")
			cmds.connectAttr(p+".rx",u+".input")

		print "//////////纠正完成---------"


def Option_two_group(obj):

	cmds.group(n=(obj+"_C"),em=True)
	cmds.group(n=(obj+"_G"))
	cmds.parentConstraint(obj,(obj+"_G"),n=(obj+"_G_par"),weight=1)
	cmds.delete((obj+"_G_par"))
	cmds.parent(obj,(obj+"_C"))

	return obj+"_G"

def Option_Locator(num):

	l = cmds.spaceLocator()[0]

	[cmds.setAttr(str(x)+ "." +a,0.1*num) for x in [l,] for a in ["sx","sy","sz"] ]
	attr = [a + x for a in ["r","s"] for x in ["x","y","z"] ]+["v"]
	[ cmds.setAttr(x + "." + a,lock=1,keyable=0,channelBox=0) for x in [l,] for a in attr]
	g = cmds.group(em=1)
	cmds.parent(l,g)

	return [l,g]

def Option_CreateChestJoint(num):

	if cmds.objExists("Chest_M"):

		p1 = cmds.xform("Chest_M",q=1,ws=1,t=1)
		p2 = [0.11*num,1.38*num,0.04*num]
		p3 = [0.08*num,1.31*num,0.08*num]

		j1 = cmds.joint(p=p1)
		j2 = cmds.joint(p=p2)
		cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
		j3 = cmds.joint(p=p3)
		cmds.joint(j2,e=1,zso=1,oj="xyz",sao="yup")

		[cmds.setAttr(x+".radi",num) for x in [j1,j2,j3] ]

		l1 = Option_Locator(num)
		l2 = Option_Locator(num)

		

		cmds.delete(cmds.pointConstraint(j2,l1[1],weight=1) )
		cmds.pointConstraint(l1[0],j2,mo=1,weight=1)

		cmds.delete( cmds.pointConstraint(j3,l2[1],weight=1) )
		cmds.pointConstraint(l2[0],j3,mo=1,weight=1)

		if not cmds.objExists("Chest_M_all_G"):
			cmds.group(n="Chest_M_all_G",em=1)

		[ cmds.parent(x,"Chest_M_all_G") for x in [j1,l1[1],l2[1]] ]
		cmds.select(cl=1)

		return "Chest_M_all_G"



def Option_doItChestLine():

	if cmds.objExists("Chest_M_all_G"):

		chestJoint = cmds.listRelatives("Chest_M_all_G",c=1,type="joint")[0]
		j = cmds.listRelatives(chestJoint,ad=1,type="joint")

		p1 = cmds.xform(chestJoint,q=1,ws=1,t=1)
		p2 = cmds.xform(j[1],q=1,ws=1,t=1)
		p3 = cmds.xform(j[0],q=1,ws=1,t=1)

		cmds.delete("Chest_M_all_G")

		j1 = cmds.joint(n="Left_bosomA_joint1",p=p1)
		j2 = cmds.joint(n="Left_bosomA_joint2",p=p2)
		cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
		j3 = cmds.joint(n="Left_bosomA_joint3",p=p3)
		cmds.joint(j2,e=1,zso=1,oj="xyz",sao="yup")
		j4 = cmds.joint(n="Left_bosomA_joint4",p=p3)
		cmds.joint(j3,e=1,zso=1,oj="xyz",sao="yup")
		cmds.select(cl=1)
		cmds.setAttr(j3+".drawStyle",2)

		cmds.setAttr(j4+".ry",-90)
		cmds.makeIdentity(j4,apply=1,r=1,n=0,pn=1)

		n = [(x-y)/3.0 for x,y in zip(p2,p3)]
		p4 = [x-y for x,y in zip(p2,n)]
		p5 = [x-y for x,y in zip(p4,n)]

		j1_B = cmds.joint(n="Left_bosomB_joint1",p=p1)
		j2_B = cmds.joint(n="Left_bosomB_joint2",p=p4)
		cmds.joint(j1_B,e=1,zso=1,oj="xyz",sao="yup")

		cmds.select(cl=1)

		j1_C = cmds.joint(n="Left_bosomC_joint1",p=p1)
		j2_C = cmds.joint(n="Left_bosomC_joint2",p=p5)
		cmds.joint(j1_C,e=1,zso=1,oj="xyz",sao="yup")

		cmds.select(cl=1)

		[cmds.mirrorJoint(x,mirrorYZ=1,mirrorBehavior=1,searchReplace=("Left","Right")) for x in [j1,j1_B,j1_C] ]

		ikH1 = cmds.ikHandle(sj=j2,ee=j3,n="Left_bosomA_ikHandle1")[0]
		ikH2 = cmds.ikHandle(sj=j1_B,ee=j2_B,n="Left_bosomB_ikHandle1")[0]
		ikH3 = cmds.ikHandle(sj=j1_C,ee=j2_C,n="Left_bosomC_ikHandle1")[0]

		ctrl = option_createCircle("Left_bosomA")
		cmds.delete(cmds.parentConstraint(j4,ctrl[1]))

		[ cmds.parentConstraint(j2,x,mo=1) for x in [ikH2,ikH3] ]
		[ cmds.parentConstraint(ctrl[0],x,mo=1) for x in [ikH1,j4]]

		up = cmds.group(n="Left_bosom_Aim_up",em=1)
		up_g = cmds.group(n="Left_bosom_Aim_up_g",em=1)
		cmds.parent(up,up_g)
		cmds.delete( cmds.parentConstraint(j1,up_g,weight=1))
		cmds.setAttr(up+".ty",0.05)
		cmds.parent(up,w=1)
		cmds.delete(up_g)

		j1_r = j1.replace("Left","Right")
		j2_r = j2.replace("Left","Right")
		j3_r = j3.replace("Left","Right")
		j4_r = j4.replace("Left","Right")
		cmds.setAttr(j3_r+".drawStyle",2)

		j1_B_r = j1_B.replace("Left","Right")
		j2_B_r = j2_B.replace("Left","Right")
		j1_C_r = j1_C.replace("Left","Right")
		j2_C_r = j2_C.replace("Left","Right")

		ikH1_r = cmds.ikHandle(sj=j2_r,ee=j3_r,n="Right_bosomA_ikHandle1")[0]
		ikH2_r = cmds.ikHandle(sj=j1_B_r,ee=j2_B_r,n="Right_bosomB_ikHandle1")[0]
		ikH3_r = cmds.ikHandle(sj=j1_C_r,ee=j2_C_r,n="Right_bosomC_ikHandle1")[0]

		ctrl_r = option_createCircle("Right_bosomA")
		cmds.delete(cmds.parentConstraint(j4_r,ctrl_r[1]))

		[ cmds.parentConstraint(j2_r,x,mo=1) for x in [ikH2_r,ikH3_r] ]
		[ cmds.parentConstraint(ctrl_r[0],x,mo=1) for x in [ikH1_r,j4_r]]

		up_r = cmds.group(n="Right_bosom_Aim_up",em=1)
		up_g_r = cmds.group(n="Right_bosom_Aim_up_g")
		cmds.select(cl=1)
		cmds.delete( cmds.parentConstraint(j1_r,up_g_r,weight=1))
		cmds.setAttr(up_r+".ty",-0.05)
		cmds.parent(up_r,w=1)
		cmds.delete(up_g_r)

		if cmds.objExists("Shoulder_L_optionAim"):
			cmds.aimConstraint("Shoulder_L_optionAim",j1,mo=1,weight=1,aimVector=(1,0,0) ,upVector=(0,1,0),worldUpType="object",worldUpObject=up)
		if cmds.objExists("Shoulder_R_optionAim"):
			cmds.aimConstraint("Shoulder_R_optionAim",j1_r,mo=1,weight=1,aimVector=(1,0,0) ,upVector=(0,1,0),worldUpType="object",worldUpObject=up_r)


		if not cmds.objExists("Left_bosom_G"):
			cmds.group(n="Left_bosom_G",em=1)

		cmds.parent([j1,j1_B,j1_C,ctrl[1],ikH1,ikH2,ikH3,up],"Left_bosom_G")

		if not cmds.objExists("Right_bosom_G"):
			cmds.group(n="Right_bosom_G",em=1)

		cmds.parent([j1_r,j1_B_r,j1_C_r,ctrl_r[1],ikH1_r,ikH2_r,ikH3_r,up_r],"Right_bosom_G")
		cmds.select(cl=1)

		[cmds.setAttr(x+".v",0) for x in [ikH1_r,ikH2_r,ikH3_r,up_r,ikH1,ikH2,ikH3,up] ]

		if cmds.objExists("optionYiIK_G"):
			cmds.parent(("Left_bosom_G","Right_bosom_G"),"optionYiIK_G")

		[cmds.setAttr(x+".radi",getNum.num) for x in [j1,j2,j3,j4,j1_B,j2_B,j1_C,j2_C] ]

		[cmds.parentConstraint("Chest_M",x,mo=1,weight=1) for x in ["Left_bosom_G","Right_bosom_G"] if cmds.objExists(x) and cmds.objExists("Chest_M")]


def Option_potionJoint(num,p1,p2,name):

	cmds.select(cl=1)
	j1 = cmds.joint(p=p1,n=name+"_YI_joint1")
	j2 = cmds.joint(p=p2,n=name+"_YI_joint2")
	cmds.joint(j1,e=1,zso=1,oj="xyz",sao="yup")
	cmds.select(cl=1)

	[cmds.setAttr(x+".radi",num) for x in [j1,j2]]

	l1 = Option_Locator(num)
	l2 = Option_Locator(num)

	cmds.delete(cmds.pointConstraint(j1,l1[1],weight=1))
	cmds.pointConstraint(l1[0],j1,mo=1,weight=1)

	cmds.delete(cmds.pointConstraint(j2,l2[1],weight=1))
	cmds.pointConstraint(l2[0],j2,mo=1,weight=1)

	if not cmds.objExists("YI_all_G"):
		cmds.group(n="YI_all_G",em=1)

	[cmds.parent(x,"YI_all_G") for x in [j1,l1[1],l2[1]] ]
	cmds.select(cl=1)

	return "YI_all_G"

def Option_CreateADVYIoint(num):

	p= [[[0.05*num,1.3*num,0.01*num],[0.15*num,1.37*num,0.01*num]],[[0.04*num,1.45*num,-0.01*num],[0.08*num,1.48*num,-0.01*num]],[[0.07*num,1.4*num,-0.03*num],[0.10*num,1.33*num,-0.11*num]],[[0.05*num,1.09*num,-0.04*num],[0.10*num,1.27*num,-0.05*num]]]
	allName = ["Left_bosomB","Left_neck","Left_backA","Left_backB"]
	YI_all = [Option_potionJoint(num,x[0],x[1],y) for x,y in zip(p,allName)][0]

	return YI_all

def Option_ADVJointYiLine(na,aim,allJnt):

		cmds.select(cl=1)
		aimObj = aim

		if len(allJnt) == 1:
			if cmds.objExists(na + "_Option_YiIK_G") == True:
				name = None
			else:
				name = na + "_Option"

		all = allJnt
		g = [] 
		for j in all:
			j1 = j
			j2 = cmds.listRelatives(j1,c=1)[0]
			g.append(option_doItYiJointLine(name,aimObj,j1,j2))
			cmds.delete(j)

		return g

def Option_AdvYiLine(obj,aim):

	allJnt_r = []

	jnt = cmds.mirrorJoint(obj,mirrorYZ=1,mirrorBehavior=1,searchReplace =("Left","Right"))[0]
	jnt1 = cmds.listRelatives(jnt,c=1,type="joint")[0]

	Mir1 = jnt + "_Mirror1"
	Mir2 = jnt1 + "_Mirror2"

	cmds.rename(jnt,Mir1)
	cmds.rename(jnt1,Mir2)

	allJnt_r.append(Mir1)
	aim_r = aim.replace("L","R")
	j_r = allJnt_r[0].split("_YI_")[0]
	j_l = obj.split("_YI_")[0]

	r = Option_ADVJointYiLine(j_r,aim=aim_r,allJnt=allJnt_r)

	l = Option_ADVJointYiLine(j_l,aim=aim,allJnt=[obj,])

	return r+l

def Option_doItAdvYiLine():

	if cmds.objExists("YI_all_G"):
		allJoint = cmds.listRelatives("YI_all_G",c=1,type="joint")

		bYI = ["Left_bosomB_YI_joint1","Left_backA_YI_joint1","Left_backB_YI_joint1"]

		yiIk = []

		for x in bYI:
			if x in allJoint:
				if cmds.objExists("Shoulder_L"):
					yiIk.append( Option_AdvYiLine(x,"Shoulder_L") )

		if "Left_neck_YI_joint1" in allJoint:
			if cmds.objExists("Neck1_M"):
				yiIk.append( Option_AdvYiLine("Left_neck_YI_joint1","Neck1_M") )

		[cmds.delete(x) for x in ["Left_backA_Option_mul","Left_backB_Option_mul","Right_backA_Option_mul","Right_backB_Option_mul","Left_neck_Option_mul","Right_neck_Option_mul"] if cmds.objExists(x)]

		[cmds.parentConstraint("Chest_M",x,mo=1,weight=1) for x in ["Right_bosomB_Option_YiIK_G","Left_bosomB_Option_YiIK_G","Right_backA_Option_YiIK_G","Left_backA_Option_YiIK_G","Right_neck_Option_YiIK_G","Left_neck_Option_YiIK_G"] if cmds.objExists(x) and cmds.objExists("Chest_M")]
		[cmds.parentConstraint("Spine1_M",x,mo=1,weight=1) for x in ["Right_backB_Option_YiIK_G","Left_backB_Option_YiIK_G"] if cmds.objExists(x) and cmds.objExists("Spine1_M")]
		
		cmds.delete("YI_all_G")
		if not cmds.objExists("optionYiIK_G"):
			g = cmds.group(n="optionYiIK_G",em=1)
			[cmds.parent(x,g) for x in yiIk ]
		else:
			g ="optionYiIK_G"

		yiJoint = cmds.listRelatives("optionYiIK_G",ad=1,type="joint")
		[cmds.setAttr(x+".radi",getNum.num) for x in yiJoint]
		
		ro_neck = ["Left_neck_Option_YiIK_Ro","Right_neck_Option_YiIK_Ro"]
		aim_sh = ["Shoulder_L_optionAim","Shoulder_R_optionAim"]
		up_neck = ["Right_neck_Option_AimUp","Right_neck_Option_AimUp"]
		for i in range(0,2):
			if cmds.objExists(ro_neck[i]) and cmds.objExists(aim_sh[i]) and cmds.objExists(up_neck[i]):
				cmds.aimConstraint(aim_sh[i],ro_neck[i],mo=1,weight=1,aimVector=(1,0,0) ,upVector=(0,1,0),worldUpType="object",worldUpObject=up_neck[i])

		if cmds.objExists("Main"):
			cmds.parent(g,"Main")
			cmds.parent("optionAim_G","Main")

def Option_setCircleScale():
	if cmds.objExists("optionYiIK_G"):
		allcircle= cmds.listRelatives("optionYiIK_G",ad=1,type="nurbsCurve")
		num = getNum.num
		for c in allcircle:
			cmds.select(cl=1)
			cmds.select(cmds.listRelatives(c,p=1)[0])
			mel.eval('selectCurveCV("all")')
			cmds.scale(0.05*num,0.05*num,0.05*num)
			cmds.select(cl=1)

class getNum():
	num = 0

#def main():
	if __name__ == '__main__':
		optionUIClass()

