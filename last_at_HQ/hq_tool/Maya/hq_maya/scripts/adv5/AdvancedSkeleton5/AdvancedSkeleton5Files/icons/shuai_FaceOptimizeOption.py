#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from shiboken import wrapInstance
import faceOptimizeCommands
from faceOptimize_ui import Ui_shuaiFaceOptimizeWin
class faceOptimizeWin(Ui_shuaiFaceOptimizeWin):
    def __init__(self):
        self.allCBoxes=["shuaiChangeCtrls_checkBox","addTougueCtrls_checkBox","shuaiEyeBallCtrls_checkBox","shuaiAddScaleConstraint_checkBox","shuaiLockAndHideVisibility_checkBox"]
    def setupUI(self,shuaiFaceOptimizeWin):
        Ui_shuaiFaceOptimizeWin.setupUi(self,shuaiFaceOptimizeWin)
        self.optimizeButton.clicked.connect(self.optimize_ButtonCmd)
        self.selectAll_checkBox.stateChanged.connect(self.selectAll_checkBoxCmd)
        self.shuaiChangeCtrls_checkBox.stateChanged.connect(self.shuaiChangeCtrls_checkBoxCmd)
        self.addTougueCtrls_checkBox.stateChanged.connect(self.addTougueCtrls_checkBoxCmd)
        self.shuaiEyeBallCtrls_checkBox.stateChanged.connect(self.shuaiEyeBallCtrls_checkBoxCmd)
        self.shuaiAddScaleConstraint_checkBox.stateChanged.connect(self.shuaiAddScaleConstraint_checkBoxCmd)
        self.shuaiLockAndHideVisibility_checkBox.stateChanged.connect(self.shuaiLockAndHideVisibility_checkBoxCmd)
    
    def selectAll_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            for i in self.allCBoxes:
                if not eval('self.%s.isChecked()'%i):
                    eval('self.%s.setChecked(True)'%i)
    def shuaiChangeCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiChangeCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def addTougueCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.addTougueCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiEyeBallCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiEyeBallCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiAddScaleConstraint_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiAddScaleConstraint_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiLockAndHideVisibility_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiLockAndHideVisibility_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def optimize_ButtonCmd(self):
        self.textList=['将曲面控制器转换成曲线','添加舌头控制器','添加眼球控制器','添加缩放约束','锁定隐藏visbility属性']
        self.optimizeCmds=['faceOptimizeCommands.ChangeToCurve()','faceOptimizeCommands.adv_tongueCtrl()','faceOptimizeCommands.adv_EyeCtrl()','faceOptimizeCommands.face_Scale()','faceOptimizeCommands.adv_hideVisiblity()']
        ErrorNum=0
        print "\n==========================================开始优化==========================================\n"
        for i in range(len(self.optimizeCmds)):
            if eval('self.%s.isChecked()'%self.allCBoxes[i]):
            	errorString=self.optimize(i)
                if not errorString==None:
	                ErrorNum+=1
	                print ('错误'+str(ErrorNum)+':')
                	print '-------------------------------------------------------------------------------------------'
	                print ('****** \" %s \" 时出错，请详细查看下面的错误提示！！******'%self.textList[i])
                	print errorString
                	print '-------------------------------------------------------------------------------------------\n'
        print "==========================================优化结束==========================================\n"
        if ErrorNum==0:
            mc.warning('<<--恭喜，全部优化成功！！-->>')
        else:
            mc.warning('<<--发现有（%d）项优化失败，请打开脚本编辑器（Script Editor）查看详细失败原因-->>'%ErrorNum)
    def optimize(self,CBoxIndex):
    	try:
    		eval('%s'%self.optimizeCmds[CBoxIndex])
    	except StandardError as ErrorString:
	        return ErrorString

