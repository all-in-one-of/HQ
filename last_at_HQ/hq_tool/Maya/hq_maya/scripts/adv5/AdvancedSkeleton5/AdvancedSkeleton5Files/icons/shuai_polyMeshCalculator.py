#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
from maya.OpenMaya import *
def shuai_polyMeshCalculator():
	if mc.window('polyMeshCalculatorWin',ex=1):
		mc.deleteUI('polyMeshCalculatorWin')
	mc.window('polyMeshCalculatorWin',t='模型计算器',h=140,w=502)
	mc.columnLayout()
	mc.optionMenu('calculateModeControl' ,label='                             计算模式：',cc='shuai_polyMeshCalculator.optionChangeCmd()')
	mc.text('helpText',l=' （ 最终模型 ） 减掉 （ 蒙皮模型 ） 等于蒙皮变形前blendshape目标体模型，结果输出给 （ 输出模型 ） ',ww=1,h=40,w=500,font='fixedWidthFont')
	mc.menuItem('skinClusterInverse',label='蒙皮反算' )
	mc.menuItem('subtract',label='相减' )
	mc.menuItem('plus',label='相加')
	mc.textFieldButtonGrp('inputMeshControl1',l='最终模型：',bl='Get',bc='shuai_polyMeshCalculator.getButtonCmd(\'inputMeshControl1\')')
	mc.textFieldButtonGrp('inputMeshControl2',l='蒙皮模型：',bl='Get',bc='shuai_polyMeshCalculator.getButtonCmd(\'inputMeshControl2\')')
	mc.textFieldButtonGrp('ouputMeshControl',l='输出模型：',bl='Get',bc='shuai_polyMeshCalculator.getButtonCmd(\'ouputMeshControl\')')
	mc.button('calculate',l='运算',h=30,w=500,c='shuai_polyMeshCalculator.CalculateButtonCmd()')
	mc.showWindow('polyMeshCalculatorWin')
def optionChangeCmd():
	if mc.optionMenu('calculateModeControl',q=1,select=1)==1:
		mc.text('helpText',e=1,l=' （ 最终模型 ） 减掉 （ 蒙皮模型 ） 等于（蒙皮变形前blendshape目标体模型），结果输出给 （ 输出模型 ） ')
		mc.textFieldButtonGrp('inputMeshControl1',e=1,l='最终模型：')
		mc.textFieldButtonGrp('inputMeshControl2',e=1,l='蒙皮模型：')
	if mc.optionMenu('calculateModeControl',q=1,select=1)==2:
		mc.text('helpText',e=1,l=' （ 原始模型 ） 减掉 （ 被减模型 ） 等于（求差模型），结果输出给 （ 输出模型 ） ')
		mc.textFieldButtonGrp('inputMeshControl1',e=1,l='原始模型：')
		mc.textFieldButtonGrp('inputMeshControl2',e=1,l='被减模型：')
	if mc.optionMenu('calculateModeControl',q=1,select=1)==3:
		mc.text('helpText',e=1,l=' （ 原始模型 ） 加上 （ 相加模型 ） 等于（求和模型），结果输出给 （ 输出模型 ） ')
		mc.textFieldButtonGrp('inputMeshControl1',e=1,l='原始模型：')
		mc.textFieldButtonGrp('inputMeshControl2',e=1,l='相加模型：')
def getButtonCmd(controlName):
	objs=mc.ls(sl=1)
	for i in objs:
		shapeNode=mc.listRelatives(i,s=1)[0]
		if mc.nodeType(shapeNode)=='mesh':
			mc.textFieldButtonGrp(controlName,e=1,tx=i)
			break
def CalculateButtonCmd():
	calculateMode=mc.optionMenu('calculateModeControl',q=1,select=1)
	inputMesh1=mc.textFieldButtonGrp('inputMeshControl1',q=1,tx=1)
	inputMesh2=mc.textFieldButtonGrp('inputMeshControl2',q=1,tx=1)
	outputMesh=mc.textFieldButtonGrp('ouputMeshControl',q=1,tx=1)
	polyMeshCalculator(calculateMode,inputMesh1,inputMesh2,outputMesh)
def polyMeshCalculator(calculateMode,inputMesh1,inputMesh2,outputMesh):
	outputObj=MObject()
	inputDgPath1=MDagPath()
	inputObj2=MObject()
	skinNodeObj=MObject()
	tweakNodeObj=MObject()
	inputDgPath2=MDagPath()
	
	finalPos=MPoint()
	soucePos=MPoint()
	convertMatrix=MMatrix()
	
	selections=MSelectionList()
	selections.add(inputMesh1)
	selections.add(inputMesh2)
	selections.add(outputMesh)
	
	selections.getDependNode(2,outputObj)
	selections.getDagPath(0,inputDgPath1)
	
	fnDN=MFnDependencyNode()
	
	fnFinalMesh=MFnMesh(inputDgPath1)
	
	fnMatrix=MFnMatrixData()
	
	vtxIter=MItMeshVertex(outputObj)
	vtxIter.reset()
	
	if(calculateMode==1):
		skinClusterNodes=[]
		tweakNodes=[]
		inputs=mc.listHistory(inputMesh2)
		for i in inputs:
			if mc.nodeType(i)=='skinCluster':
				skinClusterNodes.append(i)
			if mc.nodeType(i)=='tweak':
				tweakNodes.append(i)
		if not skinClusterNodes:
			mc.error('Can\'t find any skin object!!')
		skinClusterNode=skinClusterNodes[0]
		tweakNode=tweakNodes[0]
		selections.add(skinClusterNode)
		selections.add(tweakNode)
		selections.getDependNode(1,inputObj2)
		selections.getDependNode(3,skinNodeObj)
		selections.getDependNode(4,tweakNodeObj)
		
		fnDN.setObject(skinNodeObj)
		weightListPlug=fnDN.findPlug('weightList')
		BPMatrixPlug=fnDN.findPlug('bindPreMatrix')
		matrixPlug=fnDN.findPlug('matrix')
		
		fnDN.setObject(inputObj2)
		skinObjMatrixPlug=fnDN.findPlug('worldMatrix').elementByLogicalIndex(0)
		skinMeshMatrixObj=skinObjMatrixPlug.asMObject()
		fnMatrix.setObject(skinMeshMatrixObj)
		skinMeshMatrixValue=fnMatrix.matrix()
		
		fnDN.setObject(tweakNodeObj)
		vlistPlug=fnDN.findPlug('vlist').elementByLogicalIndex(0).child(0)
		
		while not vtxIter.isDone():
			index=vtxIter.index()
			pos=vtxIter.position()
			fnFinalMesh.getPoint(index,finalPos,MSpace.kObject)
			
			infJointWeightsPlug=weightListPlug.elementByLogicalIndex(index).child(0)
			infJointNum=infJointWeightsPlug.numElements()
			convertMatrix*=0
			for i in range(infJointNum):
				infJointWeightPlug=infJointWeightsPlug.elementByPhysicalIndex(i)
				infJointIndex=infJointWeightPlug.logicalIndex()
				
				BPMatrixObj=BPMatrixPlug.elementByLogicalIndex(infJointIndex).asMObject()
				fnMatrix.setObject(BPMatrixObj)
				BPMatrixValue=fnMatrix.matrix()
				
				matrixObj=matrixPlug.elementByLogicalIndex(infJointIndex).asMObject()
				fnMatrix.setObject(matrixObj)
				matrixValue=fnMatrix.matrix()
		
				weightValue=infJointWeightsPlug.elementByLogicalIndex(infJointIndex).asDouble()
				tweakPointX=vlistPlug.elementByLogicalIndex(index).child(0).asDouble()
				tweakPointY=vlistPlug.elementByLogicalIndex(index).child(1).asDouble()
				tweakPointZ=vlistPlug.elementByLogicalIndex(index).child(2).asDouble()
				tweakPoint=MPoint(tweakPointX,tweakPointY,tweakPointZ)
				skinMatrix=BPMatrixValue*matrixValue*weightValue
				convertMatrix+=skinMatrix
			newPos=finalPos*skinMeshMatrixValue*convertMatrix.inverse()*skinMeshMatrixValue.inverse()-tweakPoint
			mc.xform(outputMesh+'.vtx[%d]'%index,os=1,a=1,t=[newPos.x,newPos.y,newPos.z])
			vtxIter.next()
	
	else:
		selections.getDagPath(1,inputDgPath2)
		fnSouceMesh=MFnMesh(inputDgPath2)
		if(calculateMode==2):
			while not vtxIter.isDone():
				index=vtxIter.index()
				pos=vtxIter.position()
				fnFinalMesh.getPoint(index,finalPos,MSpace.kObject)
				fnSouceMesh.getPoint(index,soucePos,MSpace.kObject)
				newPos=pos+MVector(finalPos)-MVector(soucePos)
				mc.xform(outputMesh+'.vtx[%d]'%index,os=1,a=1,t=[newPos.x,newPos.y,newPos.z])
				vtxIter.next()
		if(calculateMode==3):
			while not vtxIter.isDone():
				index=vtxIter.index()
				pos=vtxIter.position()
				fnFinalMesh.getPoint(index,finalPos,MSpace.kObject)
				fnSouceMesh.getPoint(index,soucePos,MSpace.kObject)
				newPos=finalPos+MVector(soucePos)-MVector(pos)
				mc.xform(outputMesh+'.vtx[%d]'%index,os=1,a=1,t=[newPos.x,newPos.y,newPos.z])
				vtxIter.next()
