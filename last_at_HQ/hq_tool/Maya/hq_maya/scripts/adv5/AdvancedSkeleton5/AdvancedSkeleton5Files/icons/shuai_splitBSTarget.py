#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
def shuai_splitBSTarget():
	if mc.window('splitStepOneWin',ex=1):
		mc.deleteUI('splitStepOneWin')
	mc.window('splitStepOneWin',t='开始',w=200,h=200,s=0)
	mc.columnLayout(rowSpacing=10)
	mc.text('    1：先选择所有目标体模型',font='fixedWidthFont')
	mc.text('    2：加选原始模型',font='fixedWidthFont')
	mc.text('    3：点击“下一步”按钮继续操作',font='fixedWidthFont')
	mc.button(l='下一步',c='shuai_splitBSTarget.stepOne()',w=200,h=50)
	mc.showWindow('splitStepOneWin')
def stepOne():
	global faceObj
	global targetObjs
	global pos
	global weightPlane
	global weightPointPosList
	allbjs=mc.ls(sl=1)
	faceObj=allbjs[-1]
	targetObjs=allbjs[:-1]
	faceObjBBox=mc.xform(faceObj,q=1,ws=1,bb=1)
	pos=[(faceObjBBox[3]-faceObjBBox[0])/2+faceObjBBox[0],(faceObjBBox[4]-faceObjBBox[1])/2+faceObjBBox[1],(faceObjBBox[5]-faceObjBBox[2])/2+faceObjBBox[2]]
	width=(faceObjBBox[3]-faceObjBBox[0])
	height=(faceObjBBox[4]-faceObjBBox[1])
	weightPlane=mc.polyPlane(w=width,h=height,sx=4,sy=1,ax=[0,0,1],cuv=2,ch=0,n='weightPlane')[0]
	mc.xform(weightPlane,ws=1,t=pos)
	try:
		for n in range(10):
			mc.xform('weightPlane.vtx[%d]'%n,os=1,t=weightPointPosList[n])
	except:
		pass
	mc.select(['weightPlane.vtx[0]','weightPlane.vtx[1]','weightPlane.vtx[5]','weightPlane.vtx[6]'],r=1)
	mc.polyColorPerVertex(rgb=[1.0,1.0,1.0],cdo=1)
	mc.select(['weightPlane.vtx[3]','weightPlane.vtx[4]','weightPlane.vtx[8]','weightPlane.vtx[9]'],r=1)
	mc.polyColorPerVertex(rgb=[0.0,0.0,0.0],cdo=1)
	mc.select(['weightPlane.vtx[2]','weightPlane.vtx[7]'],r=1)
	mc.polyColorPerVertex(rgb=[0.5,0.5,0.5],cdo=1)
	mc.select(['weightPlane.vtx[1]','weightPlane.vtx[3]','weightPlane.vtx[6]','weightPlane.vtx[8]'],r=1)
	if mc.window('splitStepTwoWin',ex=1):
		mc.deleteUI('splitStepTwoWin')
	mc.window('splitStepTwoWin',h=98,w=202,s=0)
	mc.columnLayout(rowSpacing=10)
	mc.text(' 1：通过 “ weightPlane ” 模型调整权重')
	mc.text(' 2：点击 “ 完成 ”按钮！')
	mc.button(l='完成',w=200,h=50,c='shuai_splitBSTarget.stepTwo()')
	mc.deleteUI('splitStepOneWin')
	mc.showWindow('splitStepTwoWin')
def stepTwo():
	global weightPointPosList
	weightPointPos=[[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
	for n in range(10):
		weightPointPos[n]=mc.xform('weightPlane.vtx[%d]'%n,q=1,os=1,t=1)
	weightPointPosList=	weightPointPos
	weights=[1.0,1.0,0.5,0.0,0.0,1.0,1.0,0.5,0.0,0.0]
	RootJoint=mc.joint(None,p=[-1,0,0],n='RootJoint')
	weightJoint=mc.joint(None,p=[1,0,0],n='weightJoint')
	mc.skinCluster([weightPlane,RootJoint,weightJoint],nw=1,maximumInfluences=1,dropoffRate=0.1,n='weightSkinCluster')
	for i in range(10):
	    mc.skinPercent('weightSkinCluster','weightPlane.vtx[%d]'%i,tv=[weightJoint,weights[i]])
	mc.duplicate(faceObj,n='skinFace')
	mc.scale(1,1,0,'skinFace',p=pos)
	mc.skinCluster(['skinFace',RootJoint,weightJoint],nw=1,maximumInfluences=1,dropoffRate=0.1,n='skinFaceSkinCluster')
	mc.copySkinWeights( ss='weightSkinCluster', ds='skinFaceSkinCluster', noMirror=True ,surfaceAssociation='closestPoint',influenceAssociation='oneToOne')
	faceVtxNum=mc.polyEvaluate(faceObj,v=1)
	for n in range(faceVtxNum):
	    BSWeight=mc.skinPercent('skinFaceSkinCluster','skinFace.vtx[%d]'%n,q=1,t=weightJoint,v=1)
	    for target in targetObjs:
	        TarVtxPos=mc.xform(target+'.vtx[%d]'%n,q=1,os=1,t=1)
	        SouVtxPos=mc.xform(faceObj+'.vtx[%d]'%n,q=1,os=1,t=1)
	        MoveVector=[(SouVtxPos[0]-TarVtxPos[0])*(1-BSWeight),(SouVtxPos[1]-TarVtxPos[1])*(1-BSWeight),(SouVtxPos[2]-TarVtxPos[2])*(1-BSWeight)]
	        mc.xform(target+'.vtx[%d]'%n,r=1,t=MoveVector)
	mc.delete(['weightPlane','RootJoint','weightJoint','skinFace'])
	mc.deleteUI('splitStepTwoWin')
