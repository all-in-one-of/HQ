#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
def shuai_addBlendAttr():
	global lineID
	lineID=0
	global blendAttrList
	blendAttrList=[]
	if mc.window('addBlendAttrWin',ex=1):
		mc.deleteUI('addBlendAttrWin')
	mc.window('addBlendAttrWin',t='添加融合属性面板')
	mc.columnLayout('mainLayout',rowSpacing=5)
	mc.frameLayout('atrrListLayout',bs='etchedOut',l='融合属性列表',font='fixedWidthFont',collapsable=1,borderVisible=1)
	
	mc.rowLayout('textLayout',numberOfColumns=4)
	mc.text('属性名',w=200,h=25,font='fixedWidthFont')
	mc.text('开始值',w=100,h=25,font='fixedWidthFont')
	mc.text('结束值',w=100,h=25,font='fixedWidthFont')
	mc.text('',w=100,h=25,font='fixedWidthFont')
	mc.setParent('..')
	
	mc.gridLayout(numberOfColumns=2,cellWidth=254,p='mainLayout')
	mc.button('addBlendAttrBt',l='添加融合属性',c='shuai_addBlendAttr.addBlendAttrCmd()')
	mc.button('removeAllBlendAttrBt',l='移除所有属性',c='shuai_addBlendAttr.removeAllAttrCmd()')
	mc.setParent('..')
	mc.textFieldGrp('attrName',label='融合属性名称：')
	mc.textFieldButtonGrp('blendAttrObj',label='融合属性添加到：',buttonLabel='>>',bc='shuai_addBlendAttr.getBlendAttrObjCmd()')
	mc.button('addBlendAttrToObjBt',l='添加',w=510,h=50,p='mainLayout',c='shuai_addBlendAttr.blendAttrCmd()',en=0)
	
	mc.showWindow('addBlendAttrWin')
def selectAttrWin(attrList):
	if mc.window('selectAttrWin',ex=1):
		mc.deleteUI('selectAttrWin')
	mc.window('selectAttrWin',t='选择属性面板',w=206,h=359)
	mc.columnLayout(rowSpacing=5)
	mc.text('选择需要融合的属性：',font='fixedWidthFont')
	mc.textScrollList('listCtrl',w=200,h=300,ams=1,selectIndexedItem=1,append=attrList)
	mc.rowLayout(numberOfColumns=2)
	mc.button(l='选择',w=100,h=30,c='shuai_addBlendAttr.selectAttrCmd()')
	mc.button(l='取消',w=100,h=30,c='shuai_addBlendAttr.cancelCmd()')
	mc.setParent('..')
	mc.showWindow('selectAttrWin')
def selectAttrCmd():
	attrs=mc.textScrollList('listCtrl',q=1,selectItem=1)
	for attr in attrs:
		fullAttrName=obj+'.'+attr
		if not fullAttrName in blendAttrList:
			global lineID
			lineID+=1
			blendAttrList.append(fullAttrName)
			attrLayout=mc.rowLayout('attrListLayout'+str(lineID),numberOfColumns=4,p='atrrListLayout')
			mc.textField('attrName'+str(lineID),tx=fullAttrName,annotation=fullAttrName,w=200,h=25,font='fixedWidthFont',nbg=1,ebg=0,editable=0)
			fromCtrl=mc.floatField('fromCtrl'+str(lineID),w=100,h=25,value=0.0,cc='shuai_addBlendAttr.fromValueChangeCmd(\'%s\')'%attrLayout)
			toCtrl=mc.floatField('toCtrl'+str(lineID),w=100,h=25,value=1.0,cc='shuai_addBlendAttr.toValueChangeCmd(\'%s\')'%attrLayout)
			mc.button('removeAttrButton'+str(lineID),l='移除属性',w=100,h=25,c='shuai_addBlendAttr.removeAttrCmd(\'%s\')'%attrLayout)
			mc.setParent('..')
		else:
			#mc.warning('The attribute: ( %s ) has been added to the blend atrribute list!!'%fullAttrName)
			mc.warning('所选属性已经被添加到融合属性列表中！！')
	numLayout=mc.frameLayout('atrrListLayout',q=1,numberOfChildren=1)
	if numLayout>=2 and not  mc.button('addBlendAttrToObjBt',q=1,en=1):
		mc.button('addBlendAttrToObjBt',e=1,en=1)
	mc.deleteUI('selectAttrWin')
def cancelCmd():
	mc.deleteUI('selectAttrWin')
def addBlendAttrCmd():
	global obj
	objs=mc.ls(sl=1)
	if not objs:
		mc.error('必须选择一个物体！！')
	obj=objs[0]
	attrList=mc.listAttr(obj,lf=1,o=1,k=1)
	if not attrList:
		mc.error('该物体没有可用于融合的属性！！')
	selectAttrWin(attrList)
def removeAttrCmd(layoutName):
	childCtrls=mc.rowLayout(layoutName,q=1,ca=1)
	attr=mc.textField(childCtrls[0],q=1,tx=1)
	blendAttrList.remove(attr)
	mc.deleteUI(layoutName)
	numLayout=mc.frameLayout('atrrListLayout',q=1,numberOfChildren=1)
	if numLayout<2:
		mc.button('addBlendAttrToObjBt',e=1,en=0)
def removeAllAttrCmd():
	mc.button('addBlendAttrToObjBt',e=1,en=0)
	allLayouts=mc.frameLayout('atrrListLayout',q=1,childArray=1)
	allLayouts.remove('textLayout')
	global blendAttrList
	blendAttrList=[]
	if allLayouts:
		mc.deleteUI(allLayouts)
def fromValueChangeCmd(layoutName):
	childCtrls=mc.rowLayout(layoutName,q=1,childArray=1)
	fromValue=mc.floatField(childCtrls[1],q=1,v=1)
	toValue=mc.floatField(childCtrls[2],q=1,v=1)
	if fromValue==toValue:
		fromValue-=0.01
		mc.floatField(childCtrls[1],e=1,v=fromValue)
		mc.warning('开始值不能与结束值相同！！')
def toValueChangeCmd(layoutName):
	childCtrls=mc.rowLayout(layoutName,q=1,childArray=1)
	fromValue=mc.floatField(childCtrls[1],q=1,v=1)
	toValue=mc.floatField(childCtrls[2],q=1,v=1)
	if fromValue==toValue:
		toValue+=0.01
		mc.floatField(childCtrls[2],e=1,v=toValue)
		mc.warning('开始值不能与结束值相同！！')
def getBlendAttrObjCmd():
	obj=mc.ls(sl=1)[0]
	mc.textFieldButtonGrp('blendAttrObj',e=1,tx=obj)
def blendAttrCmd():
	blendObj=mc.textFieldButtonGrp('blendAttrObj',q=1,tx=1)
	attrName=mc.textFieldGrp('attrName',q=1,tx=1)
	mc.addAttr(blendObj,ln=attrName,at='double',k=1)
	souceAttr=blendWeight()
	mc.connectAttr(souceAttr,blendObj+'.'+attrName)
	mc.select(blendObj,r=1)
def getWeight():
	attrLayouts=mc.frameLayout('atrrListLayout',q=1,childArray=1)
	attrLayouts.remove('textLayout')
	outputWeightAttrs=[]
	for i in attrLayouts:
		childCtrls=mc.rowLayout(i,q=1,childArray=1)
		attrName=mc.textField(childCtrls[0],q=1,tx=1)
		fromValue=mc.floatField(childCtrls[1],q=1,v=1)
		toValue=mc.floatField(childCtrls[2],q=1,v=1)
		valueRange=[fromValue,toValue]
		valueRange.sort()
		
		clampNode=mc.createNode('clamp')
		mc.setAttr(clampNode+'.minR',valueRange[0])
		mc.setAttr(clampNode+'.maxR',valueRange[1])
		mc.connectAttr(attrName,clampNode+'.inputR')
		
		subtractNode=mc.createNode('plusMinusAverage')
		mc.connectAttr(clampNode+'.outputR',subtractNode+'.input1D[0]')
		mc.setAttr(subtractNode+'.input1D[1]',fromValue)
		mc.setAttr(subtractNode+'.operation',2)
		
		divideNode=mc.createNode('multiplyDivide')
		mc.connectAttr(subtractNode+'.output1D',divideNode+'.input1X')
		mc.setAttr(divideNode+'.input2X',toValue-fromValue)
		mc.setAttr(divideNode+'.operation',2)
		
		outputWeightAttrs.append(divideNode+'.outputX')
	return outputWeightAttrs
def blendWeight():
	outputAttrs=getWeight()
	Power=1.0/len(outputAttrs)
	multiplyNode=mc.createNode('multiplyDivide')
	mc.connectAttr(outputAttrs[0],multiplyNode+'.input1X')
	for i in outputAttrs[1:]:
		mc.connectAttr(i,multiplyNode+'.input2X')
		tmpAttr=multiplyNode+'.outputX'
		multiplyNode=mc.createNode('multiplyDivide')
		mc.connectAttr(tmpAttr,multiplyNode+'.input1X')
	mc.setAttr(multiplyNode+'.operation',3)
	mc.setAttr(multiplyNode+'.input2X',Power)
	return (multiplyNode+'.outputX')