#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from shiboken import wrapInstance
from otherTools_ui import Ui_moreRiggingToolsWindow
import FKIK_rigUI
import growAnim
import addDynamics
import backToDynamics
import shuai_splitBSTarget
import shuai_addBlendAttr
import shuai_polyMeshCalculator
import shuai_buildBlendshapeMeshByOther
import shuai_BranchesCtrl
import shuai_creatSubCtrls
class otherToolsWin(Ui_moreRiggingToolsWindow):
	def __init__(self):
		self.rootPath='O:/hq_tool/Maya/hq_maya/scripts/adv5'
		mm.eval('source \"'+self.rootPath+'/shuaiSlideJointOptimize.mel\";')
	def setupUI(self,moreRiggingToolsWindow):
		Ui_moreRiggingToolsWindow.setupUi(self,moreRiggingToolsWindow)
		self.sliderJointOptimizeButton.clicked.connect(self.slideJointOptimize_ButtonCmd)
		self.jointRiggingButton.clicked.connect(self.jointRigCmd)
		self.growButton.clicked.connect(self.growAnimCmd)
		self.hairButton.clicked.connect(self.addDynamicsCmd)
		self.backToHairButton.clicked.connect(self.backToDynamicsCmd)
		self.BSSplitButton.clicked.connect(self.bsSplitCmd)
		self.addBlendAttrButton.clicked.connect(self.addBlendAttrCmd)
		self.geoCalculatorButton.clicked.connect(self.meshCalculatorCmd)
		self.buildBlendshapeButton.clicked.connect(self.buildBlendshapeCmd)
		self.branchesCtrlButton.clicked.connect(self.branchesCtrlCmd)
		self.creatSubCtrlsButton.clicked.connect(self.creatSubCtrlsCmd)
	def slideJointOptimize_ButtonCmd(self):
		mm.eval('shuaiSlideJointOptimize;')
	def jointRigCmd(self):
		FKIK_rigUI.FKIKRiggingWin()
	def growAnimCmd(self):
		growAnim.growAnim()
	def addDynamicsCmd(self):
		addDynamics.addDynamics()
	def backToDynamicsCmd(self):
		backToDynamics.backToDynamics()	
	def bsSplitCmd(self):
		shuai_splitBSTarget.shuai_splitBSTarget()	 
	def addBlendAttrCmd(self):
		shuai_addBlendAttr.shuai_addBlendAttr()	
	def meshCalculatorCmd(self):
		shuai_polyMeshCalculator.shuai_polyMeshCalculator()	
	def buildBlendshapeCmd(self):
		shuai_buildBlendshapeMeshByOther.shuai_buildBlendshapeMeshByOther()
	def branchesCtrlCmd(self):
		shuai_BranchesCtrl.shuai_BranchesCtrl()
	def creatSubCtrlsCmd(self):
		shuai_creatSubCtrls.shuai_creatSubCtrls()