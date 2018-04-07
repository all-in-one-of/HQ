#!usr/bin/env python
#coding:utf-8
"""
@Amend Time: 2017.4.26

@author: wangzhi
"""
import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance
import functools
import math
import os


def getMayaWindow():
	
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr:
		return wrapInstance(long(ptr) , QtGui.QWidget)
		

class MatchingModel(QtGui.QWidget):
	
	def __init__(self , parent = getMayaWindow()):
		
		self.dit = {}
		self.rootList = []
		self.allSkiList = []
		
		self.notRootList = []
		self.notSkiList = []
		
		self.title = 'Matching Model UI'
		
		self.flush()
		
		super(MatchingModel , self).__init__(parent)
		self.setWindowTitle(self.title)
		self.setObjectName(self.title)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setWindowIcon(QtGui.QIcon('C:/Program Files/Autodesk/Maya2015/icons/CloudPortal/search_glass.png'))
		
		self.groupBox = QtGui.QGroupBox(self)
		self.groupBox.setGeometry(QtCore.QRect(10, 10, 530, 260))
		
		self.label = QtGui.QLabel(unicode('匹配的模型' , 'gbk')  , self.groupBox)
		self.label.setGeometry(QtCore.QRect(10, 10, 121, 20))
		self.label.setFrameShape(QtGui.QFrame.StyledPanel)
		self.label.setFrameShadow(QtGui.QFrame.Plain)
		self.label.setAlignment(QtCore.Qt.AlignCenter)		
		
		self.listWidget = DT_ListWidget(self.groupBox)
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.listWidget.setGeometry(QtCore.QRect(10, 40, 120, 210))
		self.listWidget.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget.setLineWidth(1)
		self.listWidget.setMidLineWidth(0)
		
		self.label_2 = QtGui.QLabel(unicode('对应的相似模型' , 'gbk') ,self.groupBox)
		self.label_2.setGeometry(QtCore.QRect(140, 10, 120, 20))
		self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.label_2.setFrameShape(QtGui.QFrame.StyledPanel)
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)		
		
		self.listWidget2 = DT_ListWidget(self.groupBox)
		self.listWidget2.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.listWidget2.setGeometry(QtCore.QRect(140, 40, 120, 210))
		self.listWidget2.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget2.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget2.setLineWidth(1)
		self.listWidget2.setMidLineWidth(0)		
		
		self.label_3 = QtGui.QLabel(unicode('未发现匹配的模型' , 'gbk') ,self.groupBox)
		self.label_3.setGeometry(QtCore.QRect(270, 10, 120, 20))
		self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.label_3.setFrameShape(QtGui.QFrame.StyledPanel)
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)		
		
		self.listWidget3 = DT_ListWidget(self.groupBox)
		self.listWidget3.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.listWidget3.setGeometry(QtCore.QRect(270, 40, 120, 210))
		self.listWidget3.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget3.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget3.setLineWidth(1)
		self.listWidget3.setMidLineWidth(0)			
		
		self.label_4 = QtGui.QLabel(unicode('未发现对应的模型' , 'gbk') ,self.groupBox)
		self.label_4.setGeometry(QtCore.QRect(400, 10, 120, 20))
		self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.label_4.setFrameShape(QtGui.QFrame.StyledPanel)
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)		
		
		self.listWidget4 = DT_ListWidget(self.groupBox)
		self.listWidget4.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.listWidget4.setGeometry(QtCore.QRect(400, 40, 120, 210))
		self.listWidget4.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget4.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget4.setLineWidth(1)
		self.listWidget4.setMidLineWidth(0)
		
		self.line = QtGui.QFrame(self)
		self.line.setGeometry(QtCore.QRect(5, 270, 540, 20))
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.labelType = QtGui.QLabel(unicode('匹配模式:' , 'gbk') ,self)
		self.labelType.setGeometry(QtCore.QRect(20, 290, 60, 20))
		self.labelType.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		
		self.qComboBox = QtGui.QComboBox(self)
		self.qComboBox.setGeometry(QtCore.QRect(90, 290, 100, 20))
		self.qComboBox.addItem('Hi to Hi')
		self.qComboBox.addItem('Hi to low')
		
		self.glozeQLabel = QtGui.QLabel(self)
		self.glozeQLabel.setGeometry(QtCore.QRect(200, 290, 320, 20))
		self.glozeQLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		
		self.pushButton = QtGui.QPushButton( QtGui.QIcon('C:/Program Files/Autodesk/Maya2015/icons/CloudPortal/search_glass.png') ,unicode('匹配模型' , 'gbk') ,self)
		self.pushButton.setGeometry(QtCore.QRect(40, 320, 460, 30))
		
		self.line_2 = QtGui.QFrame(self)
		self.line_2.setGeometry(QtCore.QRect(30, 350, 481, 16))
		self.line_2.setFrameShape(QtGui.QFrame.HLine)
		self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.pushButton_2 = QtGui.QPushButton(QtGui.QIcon(':copySkinWeight.png') ,unicode('传递权重' , 'gbk') ,  self)
		self.pushButton_2.setGeometry(QtCore.QRect(70, 370, 150, 30))
		
		#self.pushButton_ski = QtGui.QPushButton(QtGui.QIcon(':copySkinWeight.png') , unicode('一传多权重' , 'gbk') , self)
		#self.pushButton_ski.setGeometry(QtCore.QRect(200, 370, 150, 30))	
			
		self.pushButton_3 = QtGui.QPushButton(QtGui.QIcon(':copyUV.png') , unicode('传递UV' , 'gbk') , self)
		self.pushButton_3.setGeometry(QtCore.QRect(310, 370, 150, 30))
		
		self.line = QtGui.QFrame(self)
		self.line.setGeometry(QtCore.QRect(5, 400, 540, 20))
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.label_5 = QtGui.QLabel(unicode('执行文件:' , 'gbk')  , self)
		self.label_5.setGeometry(QtCore.QRect(20, 420, 50, 25))
		self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		
		self.lineEdit = QtGui.QLineEdit(self)
		self.lineEdit.setGeometry(QtCore.QRect(80, 420, 300, 25))
		
		self.getFileButton = QtGui.QPushButton('getFile' ,self)
		self.getFileButton.setGeometry(QtCore.QRect(390, 420, 70, 25))
		
		self.okButton = QtGui.QPushButton('OK' ,self)
		self.okButton.setGeometry(QtCore.QRect(470, 420, 70, 25))
		
		self.resize(550, 455)
		self.setMinimumSize(QtCore.QSize(550, 455))
		self.setMaximumSize(QtCore.QSize(550, 455))
		
		self.makeConnections()
		self.initUiState()
		
	def flush(self):
		
		wins = getMayaWindow().findChildren(QtGui.QWidget , self.title) or []
		for c in wins:
			try:
				c.close()
			except:
				continue
			c.deleteLater()
	 		

	def makeConnections(self):
		self.qComboBox.currentIndexChanged.connect(self.setGloze)
		self.pushButton.clicked.connect(self.rootGeo)
		self.pushButton_2.clicked.connect(self.copySkinCluste)
		self.pushButton_3.clicked.connect(self.transferUV)
		#self.pushButton_ski.clicked.connect(self.skinDialog)
		
		self.getFileButton.clicked.connect(self.getFilePathName)
		self.okButton.clicked.connect(self.executeFile)
	
	def initUiState(self):
		self.qComboBox.setCurrentIndex(1)
		self.qComboBox.setCurrentIndex(0)

	def executeFile(self):
		txt = self.lineEdit.text()
		if txt and os.path.isfile(txt):
			type = txt.split('.')[-1]
			for key ,vlaue in self.dit.items():
				if type == 'mel':
					pm.select(key,vlaue, r =1)
					mel.eval('source "{:s}"'.format(txt))
				if type == 'py':
					pm.select(key,vlaue, r =1)
					execfile(r"{:s}".format(txt))
		
		else:
			return OpenMaya.MGlobal_displayError('{:s} : File Non Existent '.format(txt))		
	
	def transferUV(self):
		for key ,vlaue in self.dit.items():
			pm.polyTransfer(key, uv=1 ,ao = vlaue )
			pm.select(key , r =1)
			pm.cycleCheck(e=0)
			mel.eval('doBakeNonDefHistory( 1, {"prePost" });')
			OpenMaya.MGlobal_clearSelectionList()
	
	def oneToNumberSkin(self , widget = None):
		rootName = self.skilineEdit.text()
		suitedName = self.skilineEdit2.text()
		
		suitedListName = suitedName.split(',')
		suitedNode = [pm.PyNode(n) for n in suitedListName]
		
		rootSki = self.getSkinCluste(pm.PyNode(rootName)) 
		
		for node in suitedNode:
			if rootSki:
				jointlist = rootSki.getInfluence()
				if not self.getSkinCluste(node):
					s = pm.skinCluster(jointlist ,node , dr = 4.5)
					pm.copySkinWeights(ss=rootSki, ds=s, noMirror=True , sa = 'closestPoint' , ia = 'closestJoint')
				else:
					s = self.getSkinCluste(node)
					pm.copySkinWeights(ss=rootSki, ds=s, noMirror=True , sa = 'closestPoint' , ia = 'closestJoint')	
		
		widget.reject()
		
	def setSeveralText(self , widget = None):
		sel = pm.selected()
		if not sel:
			return OpenMaya.MGlobal_displayError("Please select object")
		
		name = [s.name() for s in sel if s.getShape().nodeType() == 'mesh'] 
		ctrName = ','.join(name)
		
		widget.setText(ctrName)

			
	
	def skinDialog(self):
		qDialog = QtGui.QDialog(self)
		
		groupBox = QtGui.QGroupBox(qDialog)
		groupBox.setGeometry(QtCore.QRect(5, 5, 250, 131))
		
		label = QtGui.QLabel(unicode('原模型:' , 'gbk') , groupBox)
		label.setGeometry(QtCore.QRect(5, 20, 60, 20))
		label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		self.skilineEdit = QtGui.QLineEdit(groupBox)
		self.skilineEdit.setGeometry(QtCore.QRect(75, 20, 130, 20))
		self.skilineEdit.setEnabled(False)

		self.skilineBout = QtGui.QPushButton('GET' , groupBox)
		self.skilineBout.setGeometry(QtCore.QRect(215, 20, 30, 20))
		
		label_2 = QtGui.QLabel(unicode('传递模型:' , 'gbk') , groupBox)
		label_2.setGeometry(QtCore.QRect(5, 50, 60, 20))
		label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		self.skilineEdit2 = QtGui.QLineEdit(groupBox)
		self.skilineEdit2.setGeometry(QtCore.QRect(75, 50, 131, 20))
		self.skilineEdit2.setEnabled(False)
		
		self.skilineBout2 = QtGui.QPushButton('GET' , groupBox)
		self.skilineBout2.setGeometry(QtCore.QRect(215, 50, 30, 20))

		self.skiButton = QtGui.QPushButton('OK' , groupBox)
		self.skiButton.setGeometry(QtCore.QRect(130, 90, 41, 20))
		

		self.skiButton2 = QtGui.QPushButton('Close' , groupBox)
		self.skiButton2.setGeometry(QtCore.QRect(180, 90, 41, 20))
		
		self.skilineBout.clicked.connect(functools.partial(self.setDialogText , self.skilineEdit))
		self.skilineBout2.clicked.connect(functools.partial(self.setSeveralText , self.skilineEdit2))
		
		self.skiButton.clicked.connect(functools.partial(self.oneToNumberSkin , qDialog))
		self.skiButton2.clicked.connect(qDialog.reject)
		
		qDialog.resize(260,140)
		qDialog.setMinimumSize(QtCore.QSize(260,140))
		qDialog.setMaximumSize(QtCore.QSize(260,140))
		

		qDialog.show()
	
	def copySkinCluste(self):

		'''
		for key ,vlaue in self.dit.items():
			skin = self.getSkinCluste(vlaue)
			if skin:
				jointlist = skin.getInfluence()
				skijointlist = [jnt.split(':')[-1] for jnt in jointlist]
				if not self.getSkinCluste(key):
					s = pm.skinCluster(skijointlist ,key , dr = 4.5)
					pm.copySkinWeights(ss=skin, ds=s, noMirror=True , sa = 'closestPoint' , ia = 'closestJoint')
				else:
					s = self.getSkinCluste(key)
					pm.copySkinWeights(ss=skin, ds=s, noMirror=True , sa = 'closestPoint' , ia = 'closestJoint')
			else:
				OpenMaya.MGlobal_displayInfo('{:s}: Object Not SkinCluste'.format(vlaue))
				continue
		'''
		#New apiCommand

		path = 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/rigging/modifyEditer/scripts'
		#path ='D:/Work/2017/script/py/MatchingMesh//scripts'
		mel.eval('source '+'"' + path + '/nowCopySkinWeight.mel'+'"'+';')



	def setGloze(self):
		index = self.qComboBox.currentIndex()
		if index == 0:
			self.glozeQLabel.setText(unicode('选择要匹配的未蒙皮Hi模型, 点匹配模型按钮' , 'gbk'))
		if index == 1:
			self.glozeQLabel.setText(unicode('选择要匹配的未蒙皮low模型, 点匹配模型按钮' , 'gbk'))
	
	def delectObject(self , widget = None):
		
		widgetSel = widget.selectedItems()
		
		txtList = [s.text() for s in widgetSel]
		
		for txt in txtList:
			
			keys = self.dit.keys()
			values = self.dit.values()
			
			if txt in keys:
				self.notSkiList.append(self.dit[pm.PyNode(txt)])
				self.notRootList.append(pm.PyNode(txt))
				self.dit.pop(pm.PyNode(txt))
				
			
			if txt in values:
				num = values.index(txt)
				self.notSkiList.append(pm.PyNode(txt))
				self.notRootList.append(pm.PyNode(keys[num]))
				self.dit.pop(pm.PyNode(keys[num]))
		
		
		self.overLoadingDit()
		self.overLoadingNotDit()
	
	def selectDitObject(self , widget = None):
		'''
		@widget : IAR
		'''
		OpenMaya.MGlobal_clearSelectionList()
		
		widgetSel = widget.selectedItems()
		txtList = [s.text() for s in widgetSel]
		
		keys = self.dit.keys()
		values = self.dit.values()
		
		keyAssignments = [] 
		for txt in txtList:
			if txt in keys:
				
				keyAssignments.append(self.dit[pm.PyNode(txt)])
			
			if txt in values:
				num = values.index(txt)
				keyAssignments.append(pm.PyNode(keys[num]))	
		
		pm.select(txtList , r = 1)
		pm.select(keyAssignments , tgl = 1)
			
	
	def selectObject(self , widget = None):
		'''
		@widget : IAR
		'''
		OpenMaya.MGlobal_clearSelectionList()
		
		widgetSel = widget.selectedItems()	
		txtList = [s.text() for s in widgetSel]
		
		pm.select(txtList , r = 1)

	def getFilePathName(self):
		'''
		get file name displays files matching the patterns given in the string "*.py *.mel"
		'''
		pathName = self.lineEdit.text()
		if pathName and os.path.isfile(pathName):
			pathName = pathName.replace('\\' , '/')
			ListName = pathName.split('/')
			pathName = pathName.replace(ListName[-1], '')
			fileName = QtGui.QFileDialog.getOpenFileName(dir = pathName , filter = "*.py *.mel")
		else:
			fileName = QtGui.QFileDialog.getOpenFileName(filter = "*.py *.mel")
		if os.path.isfile(fileName[0]):
			self.lineEdit.setText(fileName[0])

	"""
	#this wangZhi write script

	def conceiveDit(self):
		allMesh = [a.getParent() for a in pm.ls(type="mesh" ,ni = True,  v =1) if a.getParent().getParent().find('_feetMask_') == -1]
		self.allSkiList = [a for a in allMesh if a not in self.rootList]
		
		for indxe , name in enumerate(self.rootList):
			
			distanceList = [float(self.getTwoObjectDistance(name ,s)) for s in self.allSkiList]
			
			sortDistanceList = sorted(distanceList)
			
			num = len(sortDistanceList)/2
			
			if num <= 0:
				num = 1
			 
			lsitA = [self.allSkiList[distanceList.index(sortDistanceList[i])] for i in range(num)]
			
			area = float(self.getObjcetaCreage(name))
			
			areaList = [abs(area - float(self.getObjcetaCreage(m))) for m in lsitA]
			
			sortAreaList = sorted(areaList)
			
			num = len(sortAreaList)/2
			
			if num <= 0:
				num = 1
			
			lsitB = [lsitA[areaList.index(sortAreaList[i])] for i in range(num)]
					
			vs = [float(self.getObjcetCenterWorld2(name ,s)) for s in lsitB]
			
			vs1 = sorted(vs)
			
			if self.qComboBox.currentIndex() == 1:
				
				i = vs.index(vs1[0])
				self.dit[name] = lsitB[i]
			else:
				if  vs1[0] <= 0.02:
					i = vs.index(vs1[0])
					self.dit[name] = lsitB[i]

		"""
	
	def NewConceiveDit(self):

		allMesh = [a.getParent() for a in pm.ls(type=("mesh","nurbsSurface") ,ni = True,  v =1) if a.getParent().getParent().find('_feetMask_') == -1]
		
		newAllMesh = list(set([x for x in allMesh for y in self.rootList if self.objFirstGroup(str(x)) != self.objFirstGroup(str(y)) ]))

		self.allSkiList = [a for a in newAllMesh if a not in self.rootList]

		roltDit = {}
		if self.rootList != []:
			for i,x in enumerate(self.rootList):
				pos = pm.objectCenter(x,gl=1)
				p = [round(pi,2) for pi in pos ]
				roltDit[str(p)] = self.rootList[i]

		akltDit = {}
		if self.allSkiList != []:
			for i,x in enumerate(self.allSkiList):
				pos = pm.objectCenter(x,gl=1)
				p = [round(pi,2) for pi in pos ]
				akltDit[str(p)] = self.allSkiList[i]

		#print roltDit
		#print akltDit
		if roltDit != {} and akltDit != {}:
			for x in roltDit.keys():
				if x in akltDit.keys():
					self.dit[roltDit[x]] = akltDit[x]

		#print self.dit


	def objFirstGroup(self,obj):

		g = cmds.listRelatives(obj,ap=1,f=1)[0]
		f = g.split("|")
		if f[0] == "":
			return f[1]
		return f[0]

	def getObjcetCenterWorld2(self, obj = None, mobj = None):
		'''
		obj : node , this is the obj of the Transform node
		'''
		BoxMax1 = float(self.getObjcetToWorldDistance(obj))
		BoxMax2 = float(self.getObjcetToWorldDistance(mobj))
		vec=abs(BoxMax1-BoxMax2) 
		return vec
	
	
	def getObjcetToWorldDistance(self , obj = None):
		'''
		obj : node , this is the obj of the Transform node
		'''

		vec = self.getCenterPivot(obj)
		
		vecTo2 = [math.pow(x , 2) for x in vec] 
		vecTo = math.sqrt(sum(vecTo2))
		return vecTo
	
	def getTwoObjectDistance(self , startObject = None , endObject = None):
		startCoordinate = self.getCenterPivot(startObject)
		endCoordinate = self.getCenterPivot(endObject)
		
		marginCoordinate = [math.pow((x1 - x2) , 2) for x1 , x2 in zip(startCoordinate , endCoordinate)] 
		vec = math.sqrt(sum(marginCoordinate))
		return vec
	
	def getCenterPivot(self , object = None ):
		
		BoxMin =object.getBoundingBoxMin()
		BoxMax =object.getBoundingBoxMax()
		vec=[(v1+v2)/2.0 for v1,v2 in zip(BoxMin,BoxMax)]
		return vec
		
	
	def getObjcetaCreage(self , obj = None):
		'''
		obj : node , this is the obj of the Transform node
		'''
		Vaule = obj.boundingBoxSize.get()
		manji = Vaule.x*Vaule.y*Vaule.z
		return manji

	def getSkinCluste(self , node = None ):
		
		skin = [ski for ski in node.listHistory() if ski.nodeType() == 'skinCluster']
		
		if skin:
			return skin[0]
		else:
			return None

	def rootGeo(self):
		self.dit = {}
		self.rootList = pm.selected()
		if self.rootList == []:
			OpenMaya.MGlobal.displayError('not select mesh list')
			return

		"""
		#conceiveDit ... this wangZhi write script

		self.conceiveDit()

		"""

		#NewConceiveDit ... this Lsy write script

		self.NewConceiveDit()
		
		keys = self.dit.keys()
		values = self.dit.values()
		self.notRootList = [k for k in self.rootList if k not in keys]
		self.notSkiList = [v for v in self.allSkiList if v not in values]
		
		self.overLoadingDit()
		self.overLoadingNotDit()
		
		OpenMaya.MGlobal_clearSelectionList()
		OpenMaya.MGlobal_displayInfo('///////////\n *******构建完成*******\n  ////////////\n')				
		

	def overLoadingDit(self):
		
		self.listWidget.clear()
		for i in self.dit.keys():
			item = QtGui.QListWidgetItem(i.name())
			self.listWidget.addItem(item)

		self.listWidget2.clear()
		for i in self.dit.values():
			item2 = QtGui.QListWidgetItem(i.name())
			self.listWidget2.addItem(item2)
	
	def overLoadingNotDit(self):
	
		self.listWidget3.clear()
		for i in self.notRootList :
			item = QtGui.QListWidgetItem(i.name())
			self.listWidget3.addItem(item)

		self.listWidget4.clear()
		for i in self.notSkiList:
			item2 = QtGui.QListWidgetItem(i.name())
			self.listWidget4.addItem(item2)	
	
	
	def getSkinCluste(self , node = None ):
		
		skin = [ski for ski in node.listHistory() if ski.nodeType() == 'skinCluster']
		
		if skin:
			return skin[0]
		else:
			return None
			
	def sg_selectName(self):
		sel = pm.ls(sl=True)
		if sel:
			if sel[0].getShape().nodeType() == 'mesh' or 'nurbsSurface':
				s = sel[0].name()
				return s
		else:
			return None
	
	def contextMenuEvent(self , event):
		
		if self.listWidget.hasFocus():
			if self.listWidget.rect().contains(self.listWidget.mapFromGlobal(QtGui.QCursor.pos())):
				self.creatorMenu(self.listWidget)
		
		if self.listWidget2.hasFocus():
			if self.listWidget2.rect().contains(self.listWidget2.mapFromGlobal(QtGui.QCursor.pos())):
				self.creatorMenu(self.listWidget2)		

		if self.listWidget3.hasFocus():
			if self.listWidget3.rect().contains(self.listWidget3.mapFromGlobal(QtGui.QCursor.pos())):
				self.creatorMenu(self.listWidget3)

		if self.listWidget4.hasFocus():
			if self.listWidget4.rect().contains(self.listWidget4.mapFromGlobal(QtGui.QCursor.pos())):
				self.creatorMenu(self.listWidget4)
	
	def creatorMenu(self , parent = None):
		
		qmenu = QtGui.QMenu(self)
		
		if parent != self.listWidget3 and parent != self.listWidget4:
			qAdd = qmenu.addAction('Add')
			qmenu.addSeparator()
			qAdd.triggered.connect(self.creatorDialog)
			
		
		if parent.itemAt(parent.mapFromGlobal(QtGui.QCursor.pos())):
			qSelect = qmenu.addAction('Select')
			qSelect.triggered.connect(functools.partial(self.selectObject , parent))
			
			if parent != self.listWidget3 and parent != self.listWidget4:
				qSelectDit = qmenu.addAction('Select Dit')
				qSelectDit.triggered.connect(functools.partial(self.selectDitObject , parent))
				
				qmenu.addSeparator()
				qDelect = qmenu.addAction('Delete')
				qDelect.triggered.connect(functools.partial(self.delectObject , parent))
		
		qClear = qmenu.addAction('Clear All')
		qClear.triggered.connect(self.clearListWidgetDialog)
			
		qmenu.exec_(QtGui.QCursor.pos())
	
	def clearListWidgetDialog(self):
		self.listWidget.clear()
		self.listWidget2.clear()
		self.listWidget3.clear()
		self.listWidget4.clear()
		
		self.rootList = []
		self.allSkiList = []
		
		self.notRootList = []
		self.notSkiList = []
	
	def creatorDialog(self):
		qDialog = QtGui.QDialog(self)
		
		groupBox = QtGui.QGroupBox(qDialog)
		groupBox.setGeometry(QtCore.QRect(5, 5, 250, 131))
		
		label = QtGui.QLabel(unicode('匹配的模型:' , 'gbk') , groupBox)
		label.setGeometry(QtCore.QRect(5, 20, 60, 20))

		self.QialoglineEdit = QtGui.QLineEdit(groupBox)
		self.QialoglineEdit.setGeometry(QtCore.QRect(75, 20, 130, 20))
		self.QialoglineEdit.setEnabled(False)

		self.QialoglineBout = QtGui.QPushButton('GET' , groupBox)
		self.QialoglineBout.setGeometry(QtCore.QRect(215, 20, 30, 20))
		
		label_2 = QtGui.QLabel(unicode('对应的模型:' , 'gbk') , groupBox)
		label_2.setGeometry(QtCore.QRect(5, 50, 60, 20))

		self.QialoglineEdit2 = QtGui.QLineEdit(groupBox)
		self.QialoglineEdit2.setGeometry(QtCore.QRect(75, 50, 131, 20))
		self.QialoglineEdit2.setEnabled(False)
		
		self.QialoglineBout2 = QtGui.QPushButton('GET' , groupBox)
		self.QialoglineBout2.setGeometry(QtCore.QRect(215, 50, 30, 20))

		self.QialogButton = QtGui.QPushButton('OK' , groupBox)
		self.QialogButton.setGeometry(QtCore.QRect(130, 90, 41, 20))
		

		self.QialogButton2 = QtGui.QPushButton('Close' , groupBox)
		self.QialogButton2.setGeometry(QtCore.QRect(180, 90, 41, 20))
		
		self.QialoglineBout.clicked.connect(functools.partial(self.setDialogText , self.QialoglineEdit))
		self.QialoglineBout2.clicked.connect(functools.partial(self.setDialogText , self.QialoglineEdit2))
		
		self.QialogButton.clicked.connect(functools.partial(self.dialogAccept , qDialog))
		self.QialogButton2.clicked.connect(qDialog.reject)
		
		qDialog.resize(260,140)
		qDialog.setMinimumSize(QtCore.QSize(260,140))
		qDialog.setMaximumSize(QtCore.QSize(260,140))
		
		#qDialog.exec_()
		qDialog.show()
		
	def dialogAccept(self , widget = None):
		
		key = self.QialoglineEdit.text()
		vue = self.QialoglineEdit2.text()
		
		if pm.objExists(key):
			if pm.objExists(vue):
				if pm.PyNode(key) in self.dit:
					self.dit.pop(pm.PyNode(key))
				if pm.PyNode(key) in self.notRootList:
					self.notRootList.pop(pm.PyNode(key))
				if pm.PyNode(vue) in self.notSkiList:
					self.notSkiList.pop(pm.PyNode(key))
					
				self.dit[pm.PyNode(key)] = pm.PyNode(vue)
				
				self.overLoadingDit()
				self.overLoadingNotDit()
				
				widget.reject()
			else:
				OpenMaya.MGlobal_displayWarning('{:s} : Object Non Existent'.format(vue))
		else:
			OpenMaya.MGlobal_displayWarning('{:s} : Object Non Existent'.format(key))		
		
	def setDialogText(self , widget = None):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		widget.setText(ctrName)



class DT_ListWidget(QtGui.QListWidget):
	def __init__(self, *args, **kwargs):
		QtGui.QListWidget.__init__(self, *args, **kwargs)

	def focusOutEvent(self , event):
		QtGui.QListWidget.focusOutEvent(self , event)
		if not self.hasFocus():
			self.clearSelection()

def getKeys():

	try:
		k = []
		if a.listWidget.count():
			for i in range(a.listWidget.count()):
				k.append(a.listWidget.item(i).text())
	except:
		k = []

	keys = []
	if k != []:
		for x in k:
			keys.append(str(x))

	return keys

def getValues():

	try:
		v = []
		if a.listWidget2.count():
			for i in range(a.listWidget2.count()):
				v.append(a.listWidget2.item(i).text())
	except:
		v = []

	values = []
	if v != []:
		for x in v:
			values.append(str(x))

	return values

mel.eval('global proc string [] getK(){string $keys[] = `python("getKeys()")`;return $keys; }')
mel.eval('global proc string [] getV(){string $values[] = `python("getValues()")`;return $values; }')

def MatchingMesh():
	a = MatchingModel()
	a.show()


