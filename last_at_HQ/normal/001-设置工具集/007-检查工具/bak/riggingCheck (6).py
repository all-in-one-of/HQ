#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance
import pymel.core as pm 
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import functools
import re

def getMayaWindow():

	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr:
		return wrapInstance(long(ptr) , QtGui.QMainWindow)


def run():
	global win
	win = CleanCheckRIG(parent = getMayaWindow())
	return win.show()


class CleanCheckRIG(QtGui.QDialog):

	def __init__(self , parent = None):
		super(CleanCheckRIG , self).__init__(parent)
		self.Box_9_v = True
		
		self.keyOverName = []
		self.keyjointList = []
		self.setKeyDict = {'tx':0.0 , 'ty':0.0 , 'tz':0.0, 'rx':0.0 , 'ry':0.0 , 'rz':0.0 ,'sx':1.0 , 'sy':1.0 , 'sz':1.0 , 'v':True }

		self.QVBoxLayout = QtGui.QVBoxLayout()
		self.QVBoxLayout.setContentsMargins(5,5,5,5)
		
		self.groupBox = QtGui.QGroupBox()
		self.groupBox.setGeometry(QtCore.QRect(10, 10, 310, 491))
		self.QVBoxLayout.addWidget(self.groupBox)
		
		self.checkBox_1 = QtGui.QCheckBox(unicode('检查重命名的节点' , 'gbk') , self.groupBox)
		self.checkBox_1.setGeometry(QtCore.QRect(10, 5, 121, 20))
		
		self.checkBox_2 = QtGui.QCheckBox(unicode('检查命名不正确的Shape节点' , 'gbk') , self.groupBox)
		self.checkBox_2.setGeometry(QtCore.QRect(10, 25, 171, 20))
		        
		self.checkBox_3 = QtGui.QCheckBox(unicode('检查绑定后不干净的shape节点' , 'gbk') , self.groupBox)
		self.checkBox_3.setGeometry(QtCore.QRect(10, 45, 181, 20))
		       
		self.line = QtGui.QFrame(self.groupBox)
		self.line.setGeometry(QtCore.QRect(5, 63, 290, 20))
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.checkBox_6 = QtGui.QCheckBox(unicode('检查geo组以外的模型是否不可渲染' , 'gbk') , self.groupBox)
		self.checkBox_6.setGeometry(QtCore.QRect(10, 80, 211, 20))
		
		#self.checkBox_7 = QtGui.QCheckBox(unicode('检查Visibility=off的节点是否lock' , 'gbk') , self.groupBox)
		#self.checkBox_7.setGeometry(QtCore.QRect(10, 100, 211, 20))
		
		self.checkBox_8 = QtGui.QCheckBox(unicode('驱动,隐藏物体是否锁定或设置成了不可K帧' , 'gbk') , self.groupBox)
		self.checkBox_8.setGeometry(QtCore.QRect(10, 120, 201, 20))
		
		self.line_2 = QtGui.QFrame(self.groupBox)
		self.line_2.setGeometry(QtCore.QRect(5, 140, 290, 20))
		self.line_2.setFrameShape(QtGui.QFrame.HLine)
		self.line_2.setFrameShadow(QtGui.QFrame.Sunken)

		self.checkBox_9 = QtGui.QCheckBox(unicode('总控制器属性,颜色,关联显隐' , 'gbk') , self.groupBox)
		self.checkBox_9.setGeometry(QtCore.QRect(10, 160, 181, 20))
		
		self.checkBox_10 = QtGui.QCheckBox(unicode('RIG层级检查' , 'gbk') , self.groupBox)
		self.checkBox_10.setGeometry(QtCore.QRect(10, 180, 91, 20))
		
		self.checkBox_11 = QtGui.QCheckBox(unicode('毛发检查' , 'gbk') , self.groupBox)
		self.checkBox_11.setGeometry(QtCore.QRect(10, 200, 71, 20))
		
		self.checkBox_12 = QtGui.QCheckBox(unicode('检查头和手臂的Global属性' , 'gbk') , self.groupBox)
		self.checkBox_12.setGeometry(QtCore.QRect(10, 220, 171, 20))

		self.line_3 = QtGui.QFrame(self.groupBox)
		self.line_3.setGeometry(QtCore.QRect(5, 240, 290, 16))
		self.line_3.setFrameShape(QtGui.QFrame.HLine)
		self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.checkBox_13 = QtGui.QCheckBox(unicode('清理多余的层' , 'gbk') , self.groupBox)
		self.checkBox_13.setGeometry(QtCore.QRect(10, 260, 91, 20))

		self.checkBox_14 = QtGui.QCheckBox(unicode('清理未知节点' , 'gbk') , self.groupBox)
		self.checkBox_14.setGeometry(QtCore.QRect(10, 280, 91, 20))
		
		self.checkBox_15 = QtGui.QCheckBox(unicode('清理多余蒙皮节点' , 'gbk') , self.groupBox)
		self.checkBox_15.setGeometry(QtCore.QRect(10, 300, 121, 20))
		
		self.checkBox_16 = QtGui.QCheckBox(unicode('清理多余蒙皮影响' , 'gbk') , self.groupBox)
		self.checkBox_16.setGeometry(QtCore.QRect(10, 320, 121, 20))
		
		self.checkBox_17 = QtGui.QCheckBox(unicode('手动清理暗面模型' , 'gbk') , self.groupBox)
		self.checkBox_17.setGeometry(QtCore.QRect(10, 100, 211, 20))
		#self.checkBox_17.setGeometry(QtCore.QRect(10, 340, 121, 20))
		
		self.line_4 = QtGui.QFrame(self.groupBox)
		self.line_4.setGeometry(QtCore.QRect(5, 360, 290, 16))
		self.line_4.setFrameShape(QtGui.QFrame.HLine)
		self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.checkBox_20 = QtGui.QCheckBox(unicode('全选/全不选' , 'gbk') ,self.groupBox)
		self.checkBox_20.setGeometry(QtCore.QRect(10, 375, 91, 20))
		
		self.pushButton = QtGui.QPushButton(unicode('开始检查' , 'gbk') ,self.groupBox)
		self.pushButton.setGeometry(QtCore.QRect(10, 400, 280, 25))
		
		
		self.resize(310, 450)
		
		self.setMinimumSize(QtCore.QSize(310, 450))
		self.setMaximumSize(QtCore.QSize(310, 450))
		
		self.makeConnections()
		self.setWindowTitle("Check Rig UI")
		self.setLayout(self.QVBoxLayout)
		self.initUiState()
		self.show()


	def makeConnections(self):
		self.checkBox_20.stateChanged.connect(self.checkAllProc)
		self.pushButton.clicked.connect(self.checkNodesMain)

	def initUiState(self):
		
		self.checkBox_1.setChecked(True)
		self.checkBox_2.setChecked(True)
		self.checkBox_3.setChecked(True)
		self.checkBox_6.setChecked(True)
		#self.checkBox_7.setChecked(True)
		self.checkBox_8.setChecked(True)
		self.checkBox_9.setChecked(True)
		self.checkBox_10.setChecked(False)
		self.checkBox_11.setChecked(True)
		self.checkBox_12.setChecked(True)
		self.checkBox_13.setChecked(True)
		self.checkBox_14.setChecked(True)
		self.checkBox_15.setChecked(True)
		self.checkBox_16.setChecked(True)
		self.checkBox_17.setChecked(True)
		
	def checkAllProc(self ):
		checkBool = self.checkBox_20.isChecked()
		
		self.checkBox_1.setChecked(checkBool)
		self.checkBox_2.setChecked(checkBool)
		self.checkBox_3.setChecked(checkBool)

		self.checkBox_6.setChecked(checkBool)
		#self.checkBox_7.setChecked(checkBool)
		self.checkBox_8.setChecked(checkBool)
		self.checkBox_9.setChecked(checkBool)
		self.checkBox_10.setChecked(checkBool)
		self.checkBox_11.setChecked(checkBool)
		self.checkBox_12.setChecked(checkBool)
		self.checkBox_13.setChecked(checkBool)
		self.checkBox_14.setChecked(checkBool)
		self.checkBox_15.setChecked(checkBool)
		self.checkBox_16.setChecked(checkBool)
		self.checkBox_17.setChecked(checkBool)

		
	def checkNodesMain(self , *args):
		amount = 0
		pm.progressWindow( t = '处理中...' , ii = True , progress = amount)
		while True:
			if pm.progressWindow(q = True , isCancelled = True):
				 break 
			
			if pm.progressWindow(q = True , progress = True) >= 100:
				 break 
			
			if pm.window( 'checkWin' , ex = True):
				pm.deleteUI('checkWin' , window = True)
			
			pm.window('checkWin' , t = '节点信息' , wh = [500 , 650])
			pm.columnLayout('QlookLayout' , adj = True)
			
			checkListNum = 14
			eachCheckListLength = 100/checkListNum
			
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '重命名的节点：')
			
			if self.checkBox_1.isChecked():
				self.addFrm(self.checkOverNameAllObj , '1' , 'QlookLayout' , '重命名的节点：' )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '命名不正确的Shape：')
			
			if self.checkBox_2.isChecked():
				LayouName = self.addFrm(self.checkOverNameAllShape , '2' , 'QlookLayout' , '命名不正确的Shape：' )
				pm.button(p = LayouName , l = '修复Shape' ,c = functools.partial(self.renameWrongShape2 , LayouName) )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '绑定后不干净的shape：')
			
			if self.checkBox_3.isChecked():
				self.addFrm(self.checkRigShape , '3' , 'QlookLayout' , '绑定后不干净的shape：' )
				
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = 'geo组以外的模型是否不可渲染：')
			
			if self.checkBox_6.isChecked():
				LayouName = self.addFrm(self.checkObjectRender , '4' , 'QlookLayout' , 'geo组以外的模型是否不可渲染：' )
				pm.button(p = LayouName , l = '设置geo组以外的模型为不可渲染' ,c = functools.partial(self.setCheckObjectRender , LayouName) )


			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '驱动,隐藏的物体是否锁定并设置成了不可K帧：')
			
			if self.checkBox_8.isChecked():
				LayouName = self.addFrm(self.checkObjectSetKey , '6' , 'QlookLayout' , '驱动,隐藏的物体是否锁定并设置成了不可K帧：' )
				pm.button(p = LayouName , l = '锁定不可K帧' ,c = functools.partial(self.setObjectSetKey , LayouName) )
				
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '总控制器属性,颜色,关联显隐：')
			
			if self.checkBox_9.isChecked():
				LayouName = self.addFrm(self.checkMainCtrl , '7' , 'QlookLayout' , '总控制器属性,颜色,关联显隐：'  , False)
				if self.Box_9_v :
					pm.button(p = LayouName , l = '设置关联显隐' ,c = functools.partial(self.setCheckMainCtrl , LayouName) )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = 'RIG层级检查：')
			
			if self.checkBox_10.isChecked():
				self.addFrm(self.checkInterbedded , '8' , 'QlookLayout' , 'RIG层级检查：' , False )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '毛发检查：')
			
			if self.checkBox_11.isChecked():
				LayouName = self.addFrm(self.checkHair , '9' , 'QlookLayout' , '毛发检查：' )
				pm.button(p = LayouName , l = '设置毛发' ,c = functools.partial(self.setCheckHair , LayouName) )
				
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '检查头和手臂的Global属性：')
			
			if self.checkBox_12.isChecked():
				LayouName = self.addFrm(self.checkGlobalAttr , '10' , 'QlookLayout' , '检查头和手臂的Global属性：' , False )
				pm.button(p = LayouName , l = '设置头和手臂的Global属性' ,c = functools.partial(self.setCheckGlobalAttr , LayouName) )
				
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '清理多余的层：')
			
			if self.checkBox_13.isChecked():
				self.addFrm(self.cleanUp_SpilthLayer , '11' , 'QlookLayout' , '清理多余的层：' , False , [0 , 0.5 , 0] )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '清理未知节点：' )
			
			if self.checkBox_14.isChecked():
				self.addFrm(self.cleanUnknowNode , '12' , 'QlookLayout' , '清理未知节点：' , False , [0 , 0.5 , 0] )
				
			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '清理多余蒙皮节点：')
			
			if self.checkBox_15.isChecked():
				self.addFrm(self.cleanUnusedSkinNode , '13' , 'QlookLayout' , '清理多余蒙皮节点：' , False , [0 , 0.5 , 0] )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '清理多余蒙皮影响：')
			
			if self.checkBox_16.isChecked():
				self.addFrm(self.cleanUnsedInfluence , '14' , 'QlookLayout' , '清理多余蒙皮影响：' , False , [0 , 0.5 , 0] )

			amount += eachCheckListLength
			pm.progressWindow(e = True , progress = amount , status = '手动清理暗面模型')
			
			if self.checkBox_17.isChecked():
				self.addFrm(self.cleanFaceFixedshader , '15' , 'QlookLayout' , '手动清理暗面模型' )
	

			pm.progressWindow(e = True , progress = amount , status = '完成：')
			
			break
							
		pm.showWindow('checkWin')
			
		pm.progressWindow(endProgress=1)
	
	def addFrm(self ,fun , name = None ,  parent = None , addTitle = None  , selType = True , color = [0.719 , 0.418, 0.504]):
		overNameNode = fun()
		pm.frameLayout('Qfrm_'+name , cll = True , cl = True , bs = 'etchedIn' , p = parent , pec = self.closeFrm , bgc = color)
		if selType:
			pm.textScrollList('Qtxt_'+name , nr = 10 , ams = True , sc = functools.partial(self.selObj , 'Qtxt_'+name))
		else:
			pm.textScrollList('Qtxt_'+name , nr = 10 , ams = True)
			
		if isinstance(overNameNode ,list):
			for it in overNameNode:
				pm.textScrollList('Qtxt_'+name , e = True , append = it)
			title="("+str(len(overNameNode))+"个)" + addTitle	
				
		if isinstance(overNameNode ,int):
			title="("+str(overNameNode)+"个)" + addTitle		
		
		if not overNameNode:
			title="(0个)" + addTitle	
	
		pm.frameLayout('Qfrm_'+name , e = True , l = title)
		
		return 'Qfrm_'+name
	
	def selObj(self , tex = None , *args):
		cmds.select(cmds.textScrollList(tex,q=1,si=1))
		
	def closeFrm(self , *args):
		allFrm = pm.columnLayout('QlookLayout' , q = True , ca = True)
		for allFrmIt in allFrm:
			pm.frameLayout("checkWin|QlookLayout|"+allFrmIt , e = True , cl = True )	
		
	def checkOverNameAllObj(self):
		'''
		重命名的节点
		'''
		allNodeName  = pm.ls(dag = True)
		matching = re.compile('.+\|.+')
		overName = [s for s in allNodeName if matching.match(s.name())]
		return overName		

	def checkOverNameAllShape(self):
		'''
		命名不正确的Shape节点
		'''
		shape = pm.ls(type = ['mesh' , 'nurbsSurface' , 'nurbsCurve'])
		matchingShape = re.compile('.+Shape.+|.+Shape')
		matchingOrig = re.compile('.+Orig.+|.+Orig')
		overName = [s for s in shape if not matchingShape.match(s.name()) and not matchingOrig.match(s.name())]
		return overName
	
	def renameWrongShape2(self, layou= None , *args):
		name = self.checkOverNameAllShape()
		if name:
			for a in name:
				tname = a.getParent()
				a.rename(tname+"Shape") 
				
			pm.frameLayout(layou , e = True , l = '(0个)命名不正确的Shape：')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
		else:
			return
			
	def checkRigShape(self):
		'''
		绑定后不干净的shape
		'''
		deformers = ["skinCluster","blendShape","ffd","wrap","cluster","nonLinear","sculpt","jiggle","wire","mesh","groupParts","groupId","nCloth","squamaNode","ropeNode","verNailNode","polyTransfer","polySmoothFace"]
		deformerType = ["skinCluster","blendShape","ffd","wrap","cluster","nonLinear","sculpt","jiggle","wire"]
		all = pm.ls(type = ['mesh', 'nurbsSurface'] , ni = True)
		slipList = []
		for it in all:
			hist = it.listHistory()
			deform = [histit for histit in hist if histit.nodeType() in deformerType]
			if deform:
				if it.nodeType() == 'mesh':
					con = it.inMesh.inputs(sh = True)
				if it.nodeType() == 'nurbsSurface':
					con = it.create.inputs(sh = True)
				if con:
					if con[0].nodeType() not in deformers:
						if not re.match('.+shavedisplay.+' , it.name()):
							slipList.append(it)
		return	slipList	
		
	
	def getGeoGroup(self):
		
		trans = pm.ls('*_geo*' , type = 'transform' )
		geoName = [ts for ts in trans if len(ts.getAllParents()) == 1]
		if not geoName:
			return None
		return geoName
	
	def checkObjectNumerical(self):
		'''
		geo组下模型和组的属性是否为默认值
		'''
		overName = []
		geoName = self.getGeoGroup()
		
		if not geoName:
			return 
			
		childrenList = geoName[0].getChildren(type = 'transform' , ad = True )
		tranList = [c for c in childrenList if c.nodeType() == 'transform']
		attrs = ['.tx' , '.ty' , '.tz' , '.rx' , '.ry' , '.rz' ,'.sx' , '.sy' , '.sz']
		for t in tranList:
			for at in attrs:
				value = pm.getAttr(t + at)
				if at == '.sx' or at == '.sy' or at == '.sz':
					if value != 1:
						if t not in overName:
							overName.append(t)
				else:
					if value != 0:
						if t not in overName:
							overName.append(t)
		
		return overName
	

	
	def checkObjectPnts(self):
		'''
		模型CV点是否为默认值(0)
		'''
		overName = []
		geoName = self.getGeoGroup() 
	
		if not geoName:
			return 
			
		shapeList = [s.name() for s in pm.ls( type = 'mesh' , ni = True) if geoName[0] in s.getAllParents()]
		for shape in shapeList:
			num = cmds.getAttr(shape + '.pnts[*]')
			for i in num:
				if i != (0 , 0 , 0):
					if shape not in overName:
						overName.append(shape)
		
		return overName	
	
	
	def checkObjectRender(self):
		'''
		geo组以外的模型是否不可渲染
		'''
		overName = []
		geoName = self.getGeoGroup()
		
		if not geoName:
			return 
			
		allMesh = pm.ls(type = 'mesh' , ni = True)
		meshs = [s for s in allMesh if geoName[0] not in s.getAllParents()]
		attr = ['.castsShadows' , '.receiveShadows' , '.motionBlur' , '.smoothShading' , '.primaryVisibility' , '.visibleInReflections' , '.visibleInRefractions' , '.doubleSided']
		for m in meshs:
			for atr in attr:
				value = pm.getAttr(m + atr)
				if value != 0:
					if m not in overName:
						overName.append(m)
		
		return overName
	
	def setCheckObjectRender(self , layou= None , *args):
		name = self.checkObjectRender()
		if name:
			for s in name:
				self.setRender(s)
				
			pm.frameLayout(layou , e = True , l = '(0个)geo组以外的模型是否不可渲染')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
			
		else:
			return
		
	def setRender(self , shape = None , value = False):
		'''
		@shape : str , This is the shape is shape name 
		@value : bool , True or False
		设置shape为不可渲染
		'''
		attr = ['.castsShadows' , '.receiveShadows' , '.motionBlur' , '.smoothShading' , '.primaryVisibility' , '.visibleInReflections' , '.visibleInRefractions' , '.doubleSided']
		
		for atr in attr:
			pm.setAttr(shape + atr  , value)
			
			
				
	def checkObjectLock(self):
		'''
		Visibility=off的节点是否lock
		'''
		all = pm.ls(dag= True , type = 'transform' )
		trans = [t for t in all if pm.nodeType(t.getShape()) != 'camera' if t.nodeType() != 'ikEffector' if 'cloth_G' not in t.getAllParents()]
		visions = [tr for tr in trans if tr.v.get() == 0]
		overName = [at for at in visions if at.v.get(l = True) == False] 
		return overName
	
	def setObjectLock(self , layou = None , *args):
		name = self.checkObjectLock()
		if name:
			for s in name:
				s.v.set(l = True)
				
				
			pm.frameLayout(layou , e = True , l = '(0个)Visibility=off的节点是否lock：')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
	def checkObjectSetKey(self):
		'''
		驱动过的物体是否锁定并设置成了不可K帧。
		'''
		geoName = self.getGeoGroup()
		transList = []
		if geoName:
			allChild = [c for c in geoName[0].getChildren(ad = True , type = 'transform') if c.nodeType() == 'transform']
			allChild.append(geoName[0])
			transList = [chi for chi in allChild  if not chi.getShape()]
			for t in transList:
				attrlist = t.listAttr(k = True)
				for a in attrlist:
					a.setLocked(0)
			transList = [t.name() for t in allChild]
			
		jointSel =  cmds.ls( type = 'joint') 
		if jointSel:
			for jnt in jointSel:
				attr = cmds.listAttr(jnt , k = True)
				if attr:
					for a in attr:
						value = cmds.getAttr(jnt+'.'+a , k = True)
						if value:
							if jnt not in self.keyjointList:
								self.keyjointList.append(jnt)
								continue
					
					
		all = cmds.ls(dag= True , type = 'transform' )
		
		notMesh = [t.name() for t in pm.ls(dag= True , type = 'transform') if 'cloth_G' in t.getAllParents()]
		conList = cmds.ls( type =['constraint','joint'])
		ctrlList = [ cmds.listRelatives(s , p = True)[0] for s in  cmds.ls(type = ['nurbsCurve' ,'camera'])]
		transList = [t for t in all if t not in conList+ctrlList+notMesh+transList]
		attrs = ['t' , 'r' , 's'  ]
		
		
		for t in transList:
			attr = cmds.listAttr(t , k = True ,sn = True)
			if attr:
				for at in attr:
					if at not in self.setKeyDict.keys():
						continue
					value1 = cmds.getAttr(t +'.'+ at  , l = True)
					if not value1:
						value = cmds.getAttr(t +'.'+ at)
						if value != self.setKeyDict[at] :
							if t not in self.keyOverName:
								self.keyOverName.append(t)
								continue
						if cmds.listConnections(t +'.'+ at , s = True , d = False):
							if t not in self.keyOverName:
								self.keyOverName.append(t)
		
			for at in attrs:
				valueX = cmds.getAttr(t +'.'+ at +'x' , l = True)
				valueY = cmds.getAttr(t +'.'+ at +'y'  , l = True)
				valueZ = cmds.getAttr(t +'.'+ at +'z' , l = True)
				if valueX == True and valueX == True and valueX == True:
					continue
				if cmds.listConnections(t +'.'+ at , s = True , d = False):
					if t not in self.keyOverName:
						self.keyOverName.append(t)
					continue
				
				 
		return 	self.keyOverName+self.keyjointList
	
	def setObjectSetKey(self , layou = None , *args):
		
		if self.keyOverName:
			for a in self.keyOverName:
				attr = cmds.listAttr(a , k = True)
				for t in attr:
					cmds.setAttr(a+'.'+t , lock = True)
			self.keyOverName = []
		if self.keyjointList:
			for a in self.keyjointList:
				attr = cmds.listAttr(a , k = True)
				for t in attr:
					cmds.setAttr(a+'.'+t , k = False ,cb = True)
			self.keyjointList = []		
		pm.frameLayout(layou , e = True , l = '(0个)驱动过的物体是否锁定并设置成了不可K帧：')
		distribution = pm.frameLayout(layou , q = True , ca = True)
		pm.textScrollList(distribution[0] , e = True , ra = True)

		
			
	def checkMainCtrl(self):
		'''
		总控制器属性,颜色,关联显隐
		'''
		overText = []
		 
		ctrlCharacter = 'Character'
		ctrlName = "Main" 
				
		if not pm.objExists(ctrlCharacter):
			overText.append('没有总控制器 {0:s}'.format(ctrlCharacter))
			if not pm.objExists(ctrlName):
				overText.append('没有总控制器 {0:s}'.format(ctrlName))
			overText.append('手动自己改')
			self.Box_9_v  = False
			return overText		
		
		ctrl = pm.PyNode(ctrlName)
		if not ctrl.hasAttr('showMod'):
			overText.append('{:s} : 没有新增showMod属性'.format(ctrlName)) 
			
		if ctrl.getShape().overrideColor.get() != 13 :
			if ctrl.overrideColor.get() != 13:
				overText.append('{:s} : 没有改成红色'.format(ctrlName)) 
				
		if ctrl.hasAttr('showMod'):
			if self.getGeoGroup():
				if self.getGeoGroup()[0] not in ctrl.showMod.outputs():
					overText.append('{:s} : 没有关联geo组'.format(ctrlName))
			
		for g in ['shave_G' , 'yeti_G' , 'hair_G']:
			if pm.objExists(g):
				if len(pm.PyNode(g).getAllParents()) == 1:
					if ctrl not in pm.PyNode(g).inputs():
						overText.append('{:s} : 没有关联毛发组'.format(g))
					if ctrl.hasAttr(g.split('_G')[0]):
						if pm.PyNode(g.replace('_G' , '_show_G')) not in pm.Attribute(ctrl+'.'+g.split('_G')[0]).outputs():
							overText.append('{:s} : 没有关联毛发'.format(g.replace('_G' , '_show_G')))
						if pm.Attribute(ctrl+'.'+g.split('_G')[0]).get() != 0:
							overText.append('{:s} : 属性没有是默认值'.format(g.split('_G')[0]))
					else:
						overText.append('{:s} :属性没有'.format( g.split('_G')[0]))		
		self.Box_9_v  = True
		return overText
	
	def setCheckMainCtrl(self , layou = None , *args):
		name = self.checkMainCtrl()
		if name:
			ctrlName = "Main" if pm.objExists('Main') else 'character_ctrl'
			ctrl = pm.PyNode(ctrlName)
			if not ctrl.hasAttr('showMod'):
				ctrl.addAttr("showMod" , at = 'long' ,min= 0 , max = 1 , dv = 1 , k = True)
			ctrl.showMod.set(1)
			if ctrl.getShape().overrideColor.get() != 13 and ctrl.overrideColor.get() != 13:
				ctrl.overrideColor.set(13)
				ctrl.getShape().overrideColor.set(13)
			if self.getGeoGroup():
				if self.getGeoGroup()[0] not in ctrl.showMod.outputs():
					ctrl.showMod.connect(self.getGeoGroup()[0].v ,f = True)
			
			for g in ['shave_G' , 'yeti_G' , 'hair_G']:
				if pm.objExists(g):
					#print g
					if not pm.objExists(ctrlName+'.'+g.split('_G')[0]):
						ctrl.addAttr(g.split('_G')[0] , at = 'long' ,min= 0 , max = 1 , dv = 0 , k = True)
					attr = pm.Attribute(ctrlName+'.'+g.split('_G')[0])
					mo = pm.PyNode(g)
					mo.v.setLocked(0)
					if mo.v not in ctrl.showMod.outputs(p = True):
						ctrl.showMod.connect(mo.v ,f = True)
					mo_hair = pm.PyNode(g.replace('_G' , '_show_G'))
					mo_hair.v.setLocked(0)
					if mo_hair.v not in attr.outputs(p = True):
						attr.connect(mo_hair.v , f = True)
					mo.v.setLocked(1)
					mo_hair.v.setLocked(1)
					attr.set(0)
							
			pm.frameLayout(layou , e = True , l = '(0个)总控制器属性,颜色,关联显隐：')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
		else:
			return 
	def checkInterbedded(self):
		'''
		层级检查
		'''
		overText = []
		
		fileName = cmds.file( q =True , sn =True )
		if not fileName:
			return None
		name = fileName.split('/')[-4]
		if not pm.objExists(name+'_all') or not pm.objExists(name+'_rig') or not pm.objExists(name+'_geo'):
			 overText.append('组命名没有与文件名一致')
		
		groupList = ['Face_G' , 'Mus_G' , 'shave_G' , 'hair_G' , 'yeti_G' , 'cloth_G' , 'other_G']
		groupList += [name+'_rig' , name+'_geo']
		
		allCtrl = pm.ls('*_all' , type = 'transform')
		if allCtrl:
			cir = [s for s in allCtrl[0].getChildren() if s not in groupList]
			for i in cir :
				overText.append('有规范以外的组命名 {:s}'.format(i))
		else:
			overText.append('没有all组')
		
		return overText
	
	
	def checkHair(self):
		'''
		毛发检查
		'''
		if pm.objExists('hair_G'):
			
			hairNodeList = [h for h in pm.ls(type = 'hairSystem') if h.simulationMethod.get() != 1]
			hairNodeList = [n for n in pm.ls(type = 'nucleus') if n.enable.get() != 0]
		
			overName  = hairNodeList + hairNodeList
			return overName
		else:
			return 0
	
	def setCheckHair(self , layou = None , *args):
		name =  self.checkHair()
		if name:
			[h.simulationMethod.set(1) for h in pm.ls(type = 'hairSystem')]
			[h.enable.set(0) for h in pm.ls(type = 'nucleus')]
			
			pm.frameLayout(layou , e = True , l = '(0个)毛发检查')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
		else:
			return
		
		
	def checkGlobalAttr(self):
		'''
		检查头和手臂的Global属性默认是10，其他global属性默认是0
		'''
		overName = []
		ctrlList = [s.getParent() for s in pm.ls(dag = True , type = 'nurbsCurve')]
		isGlobalList = [c for c in ctrlList if c.hasAttr('Global')] 
		for i in isGlobalList:
			value = i.Global.get()
			if i in ['FKHead_M' , 'FKShoulder_L' , 'FKShoulder_R']:
				if value != 10:
					overName.append(i)
			else:
				if value != 0:
					overName.append(i)
					
		return overName
	
	def setCheckGlobalAttr(self , layou = None , *args):
		'''
		
		'''
		name = self.checkGlobalAttr()
		if name:
			ctrlList = [s.getParent() for s in pm.ls(dag = True , type = 'nurbsCurve')]
			isGlobalList = [c for c in ctrlList if c.hasAttr('Global')] 
			for i in isGlobalList:
				value = i.Global.get()
				if i in ['FKHead_M' , 'FKShoulder_L' , 'FKShoulder_R']:
					if value != 10:
						i.Global.set(10)
				else:
					if value != 0:
						i.Global.set(0)
						
			pm.frameLayout(layou , e = True , l = '(0个)检查头和手臂的Global属性:')
			distribution = pm.frameLayout(layou , q = True , ca = True)
			pm.textScrollList(distribution[0] , e = True , ra = True)
		else:
			return
	
	def cleanUp_SpilthLayer(self):
		'''
		清理多余的层
		'''
		LayerList =[l for l in pm.ls(type = 'displayLayer') if l.name() != 'defaultLayer']
		playLayerList1 = [l1 for l1 in LayerList if len(l1.outputs()) != 0 and l1.displayOrder.get() == 0]
		playLayerList2 = [l2 for l2 in LayerList if l2 not in playLayerList1]
		
		renderLayerList =[l for l in pm.ls(type = 'renderLayer') if l.name() != 'defaultRenderLayer']
		animLayerList = pm.ls(type =  'animLayer')
		
		overLayer =[layer.name() for layer in playLayerList2 + renderLayerList + animLayerList]
		
		
		for lay in overLayer:
			try:
				pm.delete(lay)
			except:
				pass
				
		return overLayer
	
	
	def cleanUnknowNode(self, switch = True):
		'''
		清理未知节点
		'''
		unknownList = cmds.ls(type = 'unknown')
		reNodeList = []
		nodeList = []
		
		for unknow in unknownList:
			ifRefNode = cmds.referenceQuery(unknow ,inr = True)
			if ifRefNode:
				reNodeList.append(unknow)
			
			else:
				nodeList.append(unknow)
				if switch:
					cmds.lockNode(unknow ,l = False)
					cmds.delete(unknow)
		return nodeList+reNodeList
	
	
	def cleanUnusedSkinNode(self):
		'''
		清理多余蒙皮节点
		'''
		skinList = pm.ls(type = 'skinCluster')
		checkConnection = [skin.name() for skin in skinList if len(skin.outputGeometry[0].outputs()) == 0]
		if checkConnection:
			pm.delete(lay)
		return checkConnection
	
	
	def cleanUnsedInfluence(self):
		'''
		清理多余蒙皮影响
		'''
		overName = []
		ListAllSkin = pm.ls(type = 'skinCluster')
		for skin in ListAllSkin:
			infls = skin.getInfluence() 
			wtinfs = skin.getWeightedInfluence()
			rminfs = [f for f in infls if f not in wtinfs]
			if rminfs:
				overName.append(skin)
			nodeState = skin.nodeState.get()
			skin.nodeState.set(1)
			for r in rminfs:
				pm.skinCluster(skin ,e = True , ri = r)
			skin.nodeState.set(nodeState)
		return overName
	

	def cleanFaceFixedshader(self):
		'''
		手动清理暗面模型
		'''
		#overName = []
		meshape = pm.ls(type="mesh")
		multishape = []
		for m in range(len(meshape)):
			sg = pm.listConnections(meshape[m],d=0,type="shadingEngine")
			if  sg!=[]:
				if len(sg)==1:
					if pm.listConnections(sg[0]+".surfaceShader",d=0)!=[]:
						shder =  pm.listConnections(sg[0]+".surfaceShader",d=0)[0]
						pm.select(meshape[m])
						pm.hyperShade(a = shder)
				else:
					multishape.append(meshape[m])
		
		OpenMaya.MGlobal_clearSelectionList()
		mesh = [s.getParent() for s in multishape if s.name() != 'FitEyeSphereShape' ]
		return mesh
#	def cleanUnusedShade(self):
#		'''
#		清理无链接的材质节点
#		'''
#	
#		return  mel.eval('MLdeleteUnused2()')
#	
#	def cleanDuplicateShade(self):
#		'''
#		清理重复的材质节点
#		'''
#		return mel.eval('scOpt_performOneCleanup( { "shadingNetworksOption" } );')
#	
#	def cleanLightLink(self):
#		'''
#		清理多余灯光链接
#		'''
#		return mel.eval('fh_cleanUpLightlinkers(0)')

		



