#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
def shuai_buildBlendshapeMeshByOther():
	if mc.window('buildBSWin',ex=1):
		mc.deleteUI('buildBSWin')
	mc.window('buildBSWin',t='生成blendshape目标体窗口',w=302,h=147,sizeable=0)
	mc.columnLayout(rowSpacing=5)
	mc.text('     1：先选择变体模型',font='fixedWidthFont')
	mc.text('     2：加选做好表情的角色模型',font='fixedWidthFont')
	mc.text('     注意：1:两个模型的拓扑结构要一致',font='fixedWidthFont')
	mc.text('          2:变体模型要放在与做好表情的模型\n            相同的位置',al='left',font='fixedWidthFont')
	mc.button('buildBsBT',l='生成',c='shuai_buildBlendshapeMeshByOther.buildBlendshapeMesh()',w=300,h=50)
	mc.showWindow('buildBSWin')
def buildBlendshapeMesh():
	sels=mc.ls(sl=1)
	souceObj=sels[0]
	targetObj=sels[1]
	souceShape=mc.listRelatives(souceObj,s=1,ni=1)[0]
	targetShapesWithInterObj=mc.listRelatives(targetObj,s=1)
	targetShapes=mc.listRelatives(targetObj,s=1,ni=1)
	targetOrg=None
	for i in targetShapesWithInterObj:
		if not i in targetShapes:
			targetOrg=i
	connectedAttr=mc.listConnections(targetOrg,d=1,p=1)[0]
	mc.connectAttr(souceShape+'.worldMesh[0]',connectedAttr,f=1)
	deformers=mm.eval('findRelatedDeformer %s'%targetObj)
	blendshapeNode=None
	for n in deformers:
		if mc.nodeType(n)=='blendShape':
			blendshapeNode=n
		if not mc.nodeType(n)=='blendShape' and not mc.nodeType(n)=='tweak':
			mc.setAttr(n+'.envelope',0)
	BSTargets=mc.listAttr(blendshapeNode+'.weight',m=1)
	BBox=mc.xform(targetObj,q=1,boundingBox=1)
	height=BBox[4]-BBox[1]
	weight=BBox[3]-BBox[0]
	numBS=len(BSTargets)
	souceValue=[]
	for i in range(1,numBS+1):
		souceValue.append(mc.getAttr(blendshapeNode+'.'+BSTargets[i-1]))
		mc.setAttr(blendshapeNode+'.'+BSTargets[i-1],0)
	for i in range(1,numBS+1):
		mc.setAttr(blendshapeNode+'.'+BSTargets[i-1],1)
		mc.duplicate(targetObj,n=BSTargets[i-1])
		mc.setAttr(BSTargets[i-1]+'.tx',lock=0)
		mc.setAttr(BSTargets[i-1]+'.ty',lock=0)
		mc.setAttr(BSTargets[i-1]+'.tz',lock=0)
		mc.setAttr(BSTargets[i-1]+'.rx',lock=0)
		mc.setAttr(BSTargets[i-1]+'.ry',lock=0)
		mc.setAttr(BSTargets[i-1]+'.rz',lock=0)
		mc.setAttr(BSTargets[i-1]+'.sx',lock=0)
		mc.setAttr(BSTargets[i-1]+'.sy',lock=0)
		mc.setAttr(BSTargets[i-1]+'.sz',lock=0)
		mc.parent(BSTargets[i-1],w=1)
		mc.xform(BSTargets[i-1],ws=1,t=[i*weight-((numBS+1)*weight/2),height,0])
		mc.setAttr(blendshapeNode+'.'+BSTargets[i-1],0)
	for i in range(1,numBS+1):
		souceValue.append(mc.getAttr(blendshapeNode+'.'+BSTargets[i-1]))
		mc.setAttr(blendshapeNode+'.'+BSTargets[i-1],souceValue[i-1])
	for n in deformers:
		if not mc.nodeType(n)=='blendShape' and not mc.nodeType(n)=='tweak':
			mc.setAttr(n+'.envelope',1)
	mc.connectAttr(targetOrg+'.worldMesh[0]',connectedAttr,f=1)