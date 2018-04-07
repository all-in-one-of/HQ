#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
def shuai_BranchesCtrl():
	if mc.window('addGrowBeginOffsetWin',ex=1):
		mc.deleteUI('addGrowBeginOffsetWin')
	mc.window('addGrowBeginOffsetWin',t='添加 Grow Begin Offset 属性窗口')
	mc.columnLayout()
	
	mc.rowLayout(cw1=800)
	mc.textFieldButtonGrp('allCtrlsBt',cal=[1,'right'],cw1=800,l="所有生长控制器：",buttonLabel=" >> ",w=500,bc='shuai_BranchesCtrl.getAllCtrlsBt()')
	mc.setParent('..')
	
	mc.rowLayout(cw1=800)
	mc.textFieldButtonGrp('mainCtrlBt',cal=[1,'right'],cw1=800,l="主控制器：",buttonLabel=" >> ",w=500,bc='shuai_BranchesCtrl.getMainCtrlBt()')
	mc.setParent('..')
	
	mc.rowLayout(cw1=800)
	mc.text("注意：”主控制器“必须是”所有生长控制器“中的一个！！")
	mc.setParent('..')
	
	mc.rowLayout(cw1=800)
	mc.button('setBt',l="设置",w=500,h=40,c='shuai_BranchesCtrl.addGrowBeginOffset()')
	mc.setParent('..')
	
	mc.showWindow('addGrowBeginOffsetWin')

def getAllCtrlsBt():
	Ctrls=mc.ls(sl=1)
	str=''
	for i in Ctrls:
		if not i==Ctrls[-1]:
			str+=i+';'
		else:
			str+=i
	mc.textFieldButtonGrp('allCtrlsBt',e=1,tx=str)
def getMainCtrlBt():
	Ctrl=mc.ls(sl=1)[0]
	mc.textFieldButtonGrp('mainCtrlBt',e=1,tx=Ctrl)
def addGrowBeginOffset():
	allCtrlsStr=mc.textFieldButtonGrp('allCtrlsBt',q=1,tx=1)
	allCtrls=allCtrlsStr.split(';')
	mainCtrl=mc.textFieldButtonGrp('mainCtrlBt',q=1,tx=1)
	for n in allCtrls:
		mc.addAttr(n,ln='growBeginOffset',at='double',dv=0,k=1)
		growNode=mc.listConnections(n,type='growNode')[0]
		addNode=mc.createNode('plusMinusAverage')
		mc.connectAttr(n+'.growBegin',addNode+'.input1D[0]')
		mc.connectAttr(n+'.growBeginOffset',addNode+'.input1D[1]')
		mc.connectAttr(addNode+'.output1D',growNode+'.growBegin',f=1)
		if not n==mainCtrl:
			mc.connectAttr(mainCtrl+'.growBeginOffset',n+'.growBeginOffset')
		mc.setAttr(mainCtrl+'.overrideColor',13)

	