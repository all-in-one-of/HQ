#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from shiboken import wrapInstance
from optimize_ui import Ui_shuaiAdvOptimizeWin
class optimizeWin(Ui_shuaiAdvOptimizeWin):
    def __init__(self):
        self.allCBoxes=["shuaiChangeRootCtrl_checkBox","shuaiGroupAndRename_checkBox","shuaiLockHideAttr_checkBox","chenXi_Optimize_checkBox","cc_spine2_checkBox","shuaiAddSwivelFootAttr_checkBox","shuaiFixFinggerDriven_checkBox","shuaiRotateCtrls_checkBox","shuaiAddShowModAttr_checkBox","shuaiFixConstraint_checkBox","shuaiFixCharacterScale_checkBox"]
        mm.eval('source \"O:/hq_tool/Maya/hq_maya/scripts/adv5/shuaiAdvOptimize.mel\";')
    def setupUI(self,shuaiAdvOptimizeWin):
        Ui_shuaiAdvOptimizeWin.setupUi(self,shuaiAdvOptimizeWin)
        self.optimizeButton.clicked.connect(self.optimize_ButtonCmd)
        self.selectAll_checkBox.stateChanged.connect(self.selectAll_checkBoxCmd)
        self.shuaiChangeRootCtrl_checkBox.stateChanged.connect(self.shuaiChangeRootCtrl_checkBoxCmd)
        self.shuaiGroupAndRename_checkBox.stateChanged.connect(self.shuaiGroupAndRename_checkBoxCmd)
        self.shuaiLockHideAttr_checkBox.stateChanged.connect(self.shuaiLockHideAttr_checkBoxCmd)
        self.chenXi_Optimize_checkBox.stateChanged.connect(self.chenXi_Optimize_checkBoxCmd)
        self.cc_spine2_checkBox.stateChanged.connect(self.cc_spine2_checkBoxCmd)
        self.shuaiAddSwivelFootAttr_checkBox.stateChanged.connect(self.shuaiAddSwivelFootAttr_checkBoxCmd)
        self.shuaiFixFinggerDriven_checkBox.stateChanged.connect(self.shuaiFixFinggerDriven_checkBoxCmd)
        self.shuaiRotateCtrls_checkBox.stateChanged.connect(self.shuaiRotateCtrls_checkBoxCmd)
        self.shuaiAddShowModAttr_checkBox.stateChanged.connect(self.shuaiAddShowModAttr_checkBoxCmd)
        self.shuaiFixConstraint_checkBox.stateChanged.connect(self.shuaiFixConstraint_checkBoxCmd)
        self.shuaiFixCharacterScale_checkBox.stateChanged.connect(self.shuaiFixCharacterScale_checkBoxCmd)
    def selectAll_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            for i in self.allCBoxes:
                if not eval('self.%s.isChecked()'%i):
                    eval('self.%s.setChecked(True)'%i)
                    
    def shuaiChangeRootCtrl_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiChangeRootCtrl_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiGroupAndRename_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiGroupAndRename_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiLockHideAttr_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiLockHideAttr_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def chenXi_Optimize_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.chenXi_Optimize_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def cc_spine2_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.cc_spine2_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiAddSwivelFootAttr_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiAddSwivelFootAttr_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiFixFinggerDriven_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiFixFinggerDriven_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiRotateCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiRotateCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiAddShowModAttr_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiAddShowModAttr_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)  
    def shuaiFixConstraint_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiFixConstraint_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)    
    def shuaiFixCharacterScale_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiFixCharacterScale_checkBox.isChecked():
                self.shuaiFixCharacterScale_checkBoxCmd.setChecked(False)                     
    def optimize_ButtonCmd(self):
        self.textList=['修改Root_M控制器形状','调整大组层级关系','锁定隐藏用不到的属性','调整胯部控制方式','调整身体FK控制方式','脚IK添加swivel_foot属性','修正手指驱动左右不对称','修正控制器方向','添加showMod属性','修改骨骼约束','修复Character控制器缩放']
        self.optimizeCmds=['shuaiChangeRootCtrl','shuaiGroupAndRename','shuaiLockHideAttr','chenXi_Optimize','cc_spine2','shuaiAddSwivelFootAttr','shuaiFixFinggerDriven','shuaiRotateCtrls','shuaiAddShowModAttr','orCon','shuaiConnectCharCtrlScale']
        ErrorNum=0
        errorIndex=[]
        errorString=[]
        for i in range(len(self.optimizeCmds)):
            if eval('self.%s.isChecked()'%self.allCBoxes[i]):
            	EString=self.optimize(i)
            	if not EString==None:
	            	errorString.append(EString)
	            	errorIndex.append(i)
	                ErrorNum+=1
        print "\n==========================================开始优化==========================================\n"
        for i in range(ErrorNum):
            print ('错误'+str(i+1)+':')
            print ('-------------------------------------------------------------------------------------------')
            print ('****** " %s " 时出错，请详细查看下面的错误提示！！******'%self.textList[errorIndex[i]])
            print errorString[i]
            print ('-------------------------------------------------------------------------------------------\n')
        print "==========================================优化结束==========================================\n"
        if ErrorNum==0:
            mc.warning('<<--恭喜，全部优化成功！！-->>')
        else:
            mc.warning('<<--发现有（%d）项优化失败，请打开脚本编辑器（Script Editor）查看详细失败原因-->>'%ErrorNum)
    def optimize(self,CBoxIndex):
    	if mm.eval('catch(`%s`)'%self.optimizeCmds[CBoxIndex]):
	        ErrorString=mm.eval('getLastError()')
	        return ErrorString

