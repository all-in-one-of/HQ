#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
def FKIKRiggingWin():
	ui='O:/hq_tool/Maya/hq_maya/scripts/adv5/AdvancedSkeleton5/AdvancedSkeleton5Files/icons/SkeletonRigUI.ui'
	if mc.window('SkeletonRigWindow',ex=1):
	    mc.deleteUI('SkeletonRigWindow')
	mui=mc.loadUI(f=ui)
	mc.showWindow(mui)
	mc.button('shouldButton',e=True,c='FKIK_rigUI.ShouldButtonCommand()')
	mc.button('handButton',e=True,c='FKIK_rigUI.handButtonCommand()')
	mc.button('cleanSelLabelButton',e=True,c='FKIK_rigUI.cleanSelLabelButtonCommand()')
	mc.button('cleanAllLabelButton',e=True,c='FKIK_rigUI.cleanAllLabelButtonCommand()')
	mc.button('SekeletonRigButton',e=True,c='FKIK_rigUI.SekeletonRigButtonCommand()')
def SekeletonRigButtonCommand():
    import FKIK_rig as JR
    Joints=mc.ls(sl=1,type='joint')
    for i in Joints:
        SekeletonRigButton=JR.CreatJointCtrls()
        SekeletonRigButton.CreatCtrls(i)
def ShouldButtonCommand():
    Joints=mc.ls(sl=1,type='joint')
    for i in Joints:
        mc.setAttr(i+'.drawLabel',1)
        mc.setAttr(i+'.type',10)
def handButtonCommand():
    Joints=mc.ls(sl=1,type='joint')
    for i in Joints:
        mc.setAttr(i+'.drawLabel',1)
        mc.setAttr(i+'.type',12)
def cleanSelLabelButtonCommand():
    Joints=mc.ls(sl=1,type='joint')
    for i in Joints:
        mc.setAttr(i+'.drawLabel',0)
        mc.setAttr(i+'.type',0)
def cleanAllLabelButtonCommand():
    Joints=mc.ls(type='joint')
    for i in Joints:
        mc.setAttr(i+'.drawLabel',0)
        mc.setAttr(i+'.type',0)