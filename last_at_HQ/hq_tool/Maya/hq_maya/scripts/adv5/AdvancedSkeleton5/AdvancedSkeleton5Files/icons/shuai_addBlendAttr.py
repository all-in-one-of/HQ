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
	mc.window('addBlendAttrWin',t='����ں��������')
	mc.columnLayout('mainLayout',rowSpacing=5)
	mc.frameLayout('atrrListLayout',bs='etchedOut',l='�ں������б�',font='fixedWidthFont',collapsable=1,borderVisible=1)
	
	mc.rowLayout('textLayout',numberOfColumns=4)
	mc.text('������',w=200,h=25,font='fixedWidthFont')
	mc.text('��ʼֵ',w=100,h=25,font='fixedWidthFont')
	mc.text('����ֵ',w=100,h=25,font='fixedWidthFont')
	mc.text('',w=100,h=25,font='fixedWidthFont')
	mc.setParent('..')
	
	mc.gridLayout(numberOfColumns=2,cellWidth=254,p='mainLayout')
	mc.button('addBlendAttrBt',l='����ں�����',c='shuai_addBlendAttr.addBlendAttrCmd()')
	mc.button('removeAllBlendAttrBt',l='�Ƴ���������',c='shuai_addBlendAttr.removeAllAttrCmd()')
	mc.setParent('..')
	mc.textFieldGrp('attrName',label='�ں��������ƣ�')
	mc.textFieldButtonGrp('blendAttrObj',label='�ں�������ӵ���',buttonLabel='>>',bc='shuai_addBlendAttr.getBlendAttrObjCmd()')
	mc.button('addBlendAttrToObjBt',l='���',w=510,h=50,p='mainLayout',c='shuai_addBlendAttr.blendAttrCmd()',en=0)
	
	mc.showWindow('addBlendAttrWin')
def selectAttrWin(attrList):
	if mc.window('selectAttrWin',ex=1):
		mc.deleteUI('selectAttrWin')
	mc.window('selectAttrWin',t='ѡ���������',w=206,h=359)
	mc.columnLayout(rowSpacing=5)
	mc.text('ѡ����Ҫ�ںϵ����ԣ�',font='fixedWidthFont')
	mc.textScrollList('listCtrl',w=200,h=300,ams=1,selectIndexedItem=1,append=attrList)
	mc.rowLayout(numberOfColumns=2)
	mc.button(l='ѡ��',w=100,h=30,c='shuai_addBlendAttr.selectAttrCmd()')
	mc.button(l='ȡ��',w=100,h=30,c='shuai_addBlendAttr.cancelCmd()')
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
			mc.button('removeAttrButton'+str(lineID),l='�Ƴ�����',w=100,h=25,c='shuai_addBlendAttr.removeAttrCmd(\'%s\')'%attrLayout)
			mc.setParent('..')
		else:
			#mc.warning('The attribute: ( %s ) has been added to the blend atrribute list!!'%fullAttrName)
			mc.warning('��ѡ�����Ѿ�����ӵ��ں������б��У���')
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
		mc.error('����ѡ��һ�����壡��')
	obj=objs[0]
	attrList=mc.listAttr(obj,lf=1,o=1,k=1)
	if not attrList:
		mc.error('������û�п������ںϵ����ԣ���')
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
		mc.warning('��ʼֵ���������ֵ��ͬ����')
def toValueChangeCmd(layoutName):
	childCtrls=mc.rowLayout(layoutName,q=1,childArray=1)
	fromValue=mc.floatField(childCtrls[1],q=1,v=1)
	toValue=mc.floatField(childCtrls[2],q=1,v=1)
	if fromValue==toValue:
		toValue+=0.01
		mc.floatField(childCtrls[2],e=1,v=toValue)
		mc.warning('��ʼֵ���������ֵ��ͬ����')
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