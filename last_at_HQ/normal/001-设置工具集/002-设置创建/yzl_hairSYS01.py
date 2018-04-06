#!/usr/bin/env python
#-*- coding:utf-8 -*-   
#######################
##autor<<yanzhili>>----
##ToolName<<yzl_cam>>--
##buildTime<<2010.09>>
##QQ<<342555216>>------
#######################

from maya.cmds import *
import maya.mel as MEL
import string

##
def selectJoint(first,second):
	allJoint=[]
	allJoint.append(first)	
	next=first
	nextConnect=listConnections(next+".scale",d=1,s=0)
	while(nextConnect[0]!=second):
		allJoint.append(nextConnect[0])
		nextConnect=listConnections(nextConnect[0]+".scale",d=1,s=0)
	allJoint.append(second)
	return allJoint
##
def  curveJoint(curve,num,start):
	currCurve=rebuildCurve(curve,ch=1,rpo=0,rt =0,end =1,kr =0,kcp=0,kep=1,kt=0,s=num,d=1,tol=0.01);
	select(cl=1)
	reJoint=[]
	if(start=="begin"):
		for i in range(num+1):
			vector=xform(currCurve[0]+".cv["+str(i)+"]",q=1,t=1,ws=1)
			currJoint=joint(p=(vector[0],vector[1],vector[2]),n=curve+"_skinJT"+str(i))
			reJoint.append(currJoint)
	joint(curve+"_skinJT0",e=1,oj="xyz",secondaryAxisOrient="yup",ch=1,zso=1)
	delete(currCurve)
	return reJoint

##
def createS():
	sLetter=textCurves( ch=0, f='Arial|h-13|w400|c0', t='s' )
	select(sLetter,hi=1)
	sels=ls(sl=1,type='nurbsCurve')
	reSels=pickWalk(sels[0],d="up")
	parent(reSels,w=1)
	setAttr(sels[0]+'.overrideEnabled', 1)
	setAttr(sels[0]+'.overrideColor', 17)
	delete(sLetter)
	return reSels

def getParentObject():
	sels=ls(sl=1)
	if(len(sels)>0):
		textFieldButtonGrp(parentObject,e=1,text=sels[0])
	else:
		textFieldButtonGrp(parentObject,e=1,text="")

def getJoint(num):
	sels=ls(sl=1)
	theJoint=[]
	for i in sels:
		if(nodeType(i)=="joint"):
			theJoint.append(i)
	if(len(theJoint)==2):
		if(num==0):
			textFieldButtonGrp(curve0,e=1,text=theJoint[0]+">"+theJoint[1])
		elif(num==1):
			textFieldButtonGrp(curve1,e=1,text=theJoint[0]+">"+theJoint[1])
		elif(num==2):
			textFieldButtonGrp(curve2,e=1,text=theJoint[0]+">"+theJoint[1])
	elif(len(theJoint)!=2):
		if(num==0):
			textFieldButtonGrp(curve0,e=1,text="")
		elif(num==1):
			textFieldButtonGrp(curve1,e=1,text="")
		elif(num==2):
			textFieldButtonGrp(curve2,e=1,text="")
	else:
		print "error!"
		
########	jt  A---B 	 |curveAB     	MakeCurvesDynamic() 	skin 	hiarCurveAB-hiarJointAB(IK)	
########	jt  C---D	 |curveCD   	MakeCurvesDynamic()	skin	hiarCurveCD-hiarJointCD(IK)	

def step1(jointA,jointB):
	createIkHandle=ikHandle( sj=jointA, ee=jointB, sol='ikSplineSolver',pcv=0,scv=0)
	delete(createIkHandle[0],createIkHandle[1])
	addAttr(createIkHandle[2],ln='skinJoint',at='enum',en=jointA+':'+jointB+':')
	setAttr(createIkHandle[2]+'.skinJoint',e=1,keyable=1)
	return createIkHandle[2]

def getShape(x):
	if("transform"==nodeType(x)):
		shape=listRelatives(x,fullPath=0,shapes=1)
		return shape[0]
	else:
		return None

def getTransform(x):
	if("nurbsCurve"==nodeType(x)):
		shape=listRelatives(x,fullPath=0)
		return shape[0]
	else:
		return None

def splitDian(InParamete):
	backObject=[]
	if ">" in InParamete:
		backObject=InParamete.split(">")
	return backObject

def  doHairSYS():
	allINCurve=[]
	allOutCurve=[]

	ctrS=createS()
	pObject=textFieldButtonGrp(parentObject,q=1,text=1)
	pObjectWS=xform(pObject,q=1,ws=1,t=1)
	xform(ctrS[0],ws=1,t=(pObjectWS[0],pObjectWS[1],pObjectWS[2]))
	parent(ctrS[0],pObject)

	A_=textFieldButtonGrp(curve0,q=1,text=1)
	jointA=splitDian(A_)
	if len(jointA)==2:
		allINCurve.append(step1(jointA[0],jointA[1]))

	B_=textFieldButtonGrp(curve1,q=1,text=1)
	jointB=splitDian(B_)
	if len(jointB)==2:
		allINCurve.append(step1(jointB[0],jointB[1]))

	C_=textFieldButtonGrp(curve2,q=1,text=1)
	jointC=splitDian(C_)
	if len(jointC)==2:
		allINCurve.append(step1(jointC[0],jointC[1]))
	jointNum=intSliderGrp(jointNumber,q=1,v=1)

	select(allINCurve)
	MEL.eval('assignNewHairSystem();')
	theFirstFollicle=listConnections(getShape(allINCurve[0])+".worldSpace[0]",d=1,s=0)
	theHairSystemShape=listConnections(theFirstFollicle[0]+".outHair",d=1,s=0)

	allIKs=""
	for  i in allINCurve:
		#?oint,skinCluster(joint,i)
		twoJoint=attributeQuery("skinJoint" ,node=i, listEnum=True)
		splitTwoJoint=twoJoint[0].split(":")
		skinJoint=selectJoint(splitTwoJoint[0],splitTwoJoint[1])
		skinCluster(skinJoint,i,tsb=1)
		##setFollicle
		toFollicle=listConnections(i+".worldSpace[0]",d=1,s=0)
		setAttr(toFollicle[0]+".overrideDynamics",1)	
		setAttr(toFollicle[0]+".startCurveAttract",0.1)
		#setFollicle
		##toOUTCurve
		toOutCurve=listConnections(toFollicle[0]+".outCurve",d=1,s=0)
		ikBiludJoint=curveJoint(toOutCurve[0],jointNum,"begin")
		theIK=ikHandle(sj=ikBiludJoint[0],ee=ikBiludJoint[-1],sol='ikSplineSolver',c=toOutCurve[0],ccv=0,scv=0,pcv=0)
		allIKs+=theIK[0]+":"
#
		allIkBiludJoint="";
		for n in ikBiludJoint:
			allIkBiludJoint+=n+":"
		sJ="skinJoint"+theIK[0]
		addAttr(ctrS[0],ln=sJ,at='enum',en=allIkBiludJoint)
		setAttr(ctrS[0]+'.'+sJ,e=1,keyable=1)
#
		setAttr(theIK[0]+".visibility",0)
		parent(theIK[0],theHairSystemShape[0]+"OutputCurves")
		allOutCurve.append(toOutCurve)
		setAttr( i+".inheritsTransform", 0)
		setAttr( toOutCurve[0]+".inheritsTransform" ,0)

	addAttr(ctrS[0],ln="allIKs",at='enum',en=allIKs)
	setAttr(ctrS[0]+'.allIKs',e=1,keyable=1)

	setAttr(getShape(theHairSystemShape[0])+".gravity", 0)
	setAttr(getShape(theHairSystemShape[0])+".visibility", 0)
	parent(getShape(theHairSystemShape[0]),ctrS[0],add=1,shape=1)
	print "Create Succeed! :)"


mywindow='myWindow'
if window(mywindow,exists=True):
	 deleteUI(mywindow)
mywindow=window(title="yzl-hairSYS", iconName='yzl-hairSYS', widthHeight=(200, 55),mb=1 )
menu(l='help',tearOff=0)
menuItem(l='help')
columnLayout( adjustableColumn=True )
frameLayout(l='yzlHairSYS',cll=1,cl=0,borderStyle='out')
columnLayout()
parentObject=textFieldButtonGrp( label='parentObject', buttonLabel='<<get>>',bc='getParentObject()' )
curve0=textFieldButtonGrp( label='joint[0]-start-end', buttonLabel='<<get In',bc='getJoint(0)' )
curve1=textFieldButtonGrp( label='joint[1]-start-end', buttonLabel='<<get In',bc='getJoint(1)' )
curve2=textFieldButtonGrp( label='joint[2]-start-end', buttonLabel='<<get In',bc='getJoint(2)' )
jointNumber=intSliderGrp( field=True, label='jointNumber',minValue=4, maxValue=13, fieldMinValue=3, fieldMaxValue=100, value=6)
button(w=250,l="do>>HairSYS",c="doHairSYS()")
separator( height=10,w=390, style='in' )
setParent( '..' )
setParent( '..' )
frameLayout(l='quick select',cll=1,cl=0,borderStyle='out')
columnLayout()
button(w=250,l="selectJoint_toBake",c="selectallJOINT()")
button(w=250,l="selectIK",c="selectallIK()")

setParent( '..' )
setParent( '..' )
showWindow(mywindow)

def selectallJOINT():
	sels=ls(sl=1)
	allJOINTs=[];
	for m in sels:
			prefixNamespace=get_currNameSpacePY(m)
			if(attributeQuery("allIKs",node=m,ex=1)):
				listIK=attributeQuery("allIKs",node=m,listEnum=True)
				listIKs=listIK[0].split(":")
			for i in listIKs:
				if(attributeQuery("skinJoint"+i,node=m,ex=1)):
					listAllJOINT=attributeQuery("skinJoint"+i,node=m,listEnum=True)
					listAllJOINTs=listAllJOINT[0].split(":")
					for n in listAllJOINTs:
						allJOINTs.append(prefixNamespace+n)
	select(allJOINTs)


def selectallIK():
	sels=ls(sl=1)
	allIKs=[]
	for m in sels:
		prefixNamespace=get_currNameSpacePY(m)
		if(attributeQuery("allIKs",node=m,ex=1)):
			listIK=attributeQuery("allIKs",node=m,listEnum=True)
			listIKs=listIK[0].split(":")
			for n in listIKs:
				allIKs.append(prefixNamespace+n)
	select(allIKs)


def get_currNameSpacePY(inSels):
	getNamespace="";
	tempList=inSels.split(":")
	k=len(tempList)
	if(k>1):
		for i in range(k-1):
			getNamespace+=tempList[i]+":"
		return getNamespace
	else:
		return ""

###---------------end!---------####