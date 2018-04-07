#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from shiboken import wrapInstance
import sys
path='O:/hq_tool/Maya/hq_maya/scripts/adv5/AdvancedSkeleton5/AdvancedSkeleton5Files/icons'
if not path in sys.path:
	sys.path.append(path)   
from advanceSkeleton5_ui import Ui_advancedSkeletonWin
from otherTools_ui import Ui_moreRiggingToolsWindow
from shuai_OptimizeOption import optimizeWin
from shuai_FaceOptimizeOption import faceOptimizeWin
from shuai_OtherRiggingTools import otherToolsWin
import FKIK_rigUI
import growAnim
import shuai_splitBSTarget
import shuai_addBlendAttr
import shuai_polyMeshCalculator
import shuai_animFixShapeTool
import shuai_buildBlendshapeMeshByOther
import shuai_BranchesCtrl
import shuai_creatSubCtrls
class AdvancedSkeleton5Win(Ui_advancedSkeletonWin):
    def __init__(self,advancedSkeletonWin):
    	self.rootPath='O:/hq_tool/Maya/hq_maya/scripts/adv5'
    	mm.eval('source \"'+self.rootPath+'/AdvancedSkeleton5/AdvancedSkeleton5.mel\";')
    	mm.eval('source \"'+self.rootPath+'/shuaiAdvOptimize.mel\";') 
    	mm.eval('source \"'+self.rootPath+'/shuaiBuildPose.mel\";')
    	mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    	self.QMayaWindow= wrapInstance(long(mayaMainWindowPtr), QWidget)
    	self.setupUI(advancedSkeletonWin)
    def setupUI(self,advancedSkeletonWin):
    	Ui_advancedSkeletonWin.setupUi(self,advancedSkeletonWin)
    	self.AS5_Button.clicked.connect(self.AS5_ButtonCmd)
    	self.bodySelector_Button.clicked.connect(self.bodySelector_ButtonCmd)
    	self.facialSelector_Button.clicked.connect(self.facialSelector_ButtonCmd)
    	self.bodyOptimize_Button.clicked.connect(self.bodyOptimize_ButtonCmd)
    	self.faceOptimize_Button.clicked.connect(self.faceOptimize_ButtonCmd)
    	self.IKFKSwitch_Button.clicked.connect(self.IKFKSwitch_ButtonCmd)
    	self.mocapConvert_Button.clicked.connect(self.mocapConvert_ButtonCmd)
    	self.poseDesigner_Button.clicked.connect(self.poseDesigner_ButtonCmd)
    	self.buildPose_Button.clicked.connect(self.buildPose_ButtonCmd)
    	self.moreRiggingTools_Button.clicked.connect(self.otherTools_ButtonCmd)
    	self.animFixShapeButton.clicked.connect(self.animFixShapeCmd)
        
    def AS5_ButtonCmd(self):
    	mm.eval('AdvancedSkeleton5;')
    	#mm.eval('source \"'+self.rootPath+'/AdvancedSkeleton5/install.mel\"')
    def bodySelector_ButtonCmd(self):
    	mm.eval('source \"'+self.rootPath+'/AdvancedSkeleton5/AdvancedSkeleton5Files/Selector/biped.mel\";asSelectorbiped;')
    def facialSelector_ButtonCmd(self):
    	mm.eval('source \"'+self.rootPath+'/AdvancedSkeleton5/AdvancedSkeleton5Files/Selector/face.mel\";asSelectorface;')
    def IKFKSwitch_ButtonCmd(self):
    	mm.eval('source \"'+self.rootPath+'/AdvFKIKSwitch.mel\";shuaiAdvIkFkSwitch;')  
    def mocapConvert_ButtonCmd(self):
    	mm.eval('source \"'+self.rootPath+'/advMocapConvert.mel\";shuaiMoCapToAdv;')   
    def bodyOptimize_ButtonCmd(self):
    	if(mc.window('shuaiAdvOptimizeWin',ex=1)):
    	    mc.deleteUI('shuaiAdvOptimizeWin')
    	self.QOptimizeWin=QMainWindow(self.QMayaWindow)
    	self.optimize_ui=optimizeWin()
    	self.optimize_ui.setupUI(self.QOptimizeWin)
    	self.QOptimizeWin.show()
    def faceOptimize_ButtonCmd(self):
    	if(mc.window('shuaiFaceOptimizeWin',ex=1)):
    	    mc.deleteUI('shuaiFaceOptimizeWin')
    	self.QFaceOptimizeWin=QMainWindow(self.QMayaWindow)
    	self.faceOptimize_ui=faceOptimizeWin()
    	self.faceOptimize_ui.setupUI(self.QFaceOptimizeWin)
    	self.QFaceOptimizeWin.show()
    def otherTools_ButtonCmd(self):
        if(mc.window('moreRiggingToolsWindow',ex=1)):
            mc.deleteUI('moreRiggingToolsWindow')
        self.QOtherToolsWin=QMainWindow(self.QMayaWindow)
        self.otherTools_ui=otherToolsWin()
        self.otherTools_ui.setupUI(self.QOtherToolsWin)
        self.QOtherToolsWin.show()
    def poseDesigner_ButtonCmd(self):
        mm.eval('asPoserDesigner;')
    def buildPose_ButtonCmd(self):
        mm.eval('shuaiBuildPose;')    
    def animFixShapeCmd(self):
        shuai_animFixShapeTool.shuai_animFixShapeTool()
if(mc.window('advancedSkeletonWin',ex=1)):
    mc.deleteUI('advancedSkeletonWin')
QAdvanceSleletonWin=QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget))
Adv_ui=AdvancedSkeleton5Win(QAdvanceSleletonWin)
QAdvanceSleletonWin.show()