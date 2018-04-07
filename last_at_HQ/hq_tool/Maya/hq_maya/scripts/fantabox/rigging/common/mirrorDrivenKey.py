#!usr/bin/env python
#coding:utf-8

import pymel.core as pm 
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance


def getMayaWindow():
	
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr:
		return wrapInstance(long(ptr) , QtGui.QWidget)


class MirrorDrivenKey(QtGui.QWidget):
	
	def __init__(self , parent = getMayaWindow()):
		self.mirrorNodeAttr = {}
		self.animCurveList = []
		self.nodeAttrDict = {}

		
		self.title = 'Mirror Driven Key UI'
		
		self.flush()
		
		super(MirrorDrivenKey , self).__init__(parent)
		self.setWindowTitle(self.title)
		self.setObjectName(self.title)
		self.setWindowFlags(QtCore.Qt.Window)
		
		self.winlayout = QtGui.QVBoxLayout()
		self.winlayout.setContentsMargins(5,5,5,5)
		
		self.layoutBox = QtGui.QGroupBox()
		self.winlayout.addWidget(self.layoutBox)
		self.layoutBox.setGeometry(QtCore.QRect(5, 5, 540, 420))
		
		self.groupBox = QtGui.QGroupBox(self.layoutBox)
		self.groupBox.setGeometry(QtCore.QRect(10, 50, 530, 240))
		
		self.listWidget = QtGui.QListWidget(self.groupBox)
		self.listWidget.setGeometry(QtCore.QRect(10, 40, 120, 190))
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.listWidget.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget.setLineWidth(1)
		self.listWidget.setMidLineWidth(0)
		
		self.listWidget_2 = QtGui.QListWidget(self.groupBox)
		self.listWidget_2.setGeometry(QtCore.QRect(140, 40, 120, 192))
		self.listWidget_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.listWidget_2.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget_2.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget_2.setLineWidth(1)
		self.listWidget_2.setMidLineWidth(0)
		
		self.listWidget_3 = QtGui.QListWidget(self.groupBox)
		self.listWidget_3.setGeometry(QtCore.QRect(270, 40, 120, 192))
		self.listWidget_3.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.listWidget_3.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget_3.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget_3.setLineWidth(1)
		self.listWidget_3.setMidLineWidth(0)
		
		self.listWidget_4 = QtGui.QListWidget(self.groupBox)
		self.listWidget_4.setGeometry(QtCore.QRect(400, 40, 120, 192))
		self.listWidget_4.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.listWidget_4.setFrameShape(QtGui.QFrame.WinPanel)
		self.listWidget_4.setFrameShadow(QtGui.QFrame.Raised)
		self.listWidget_4.setLineWidth(1)
		self.listWidget_4.setMidLineWidth(0)
		
		self.label_2 = QtGui.QLabel(unicode('驱动节点' , 'gbk') , self.groupBox)
		self.label_2.setGeometry(QtCore.QRect(10, 10, 120, 20))
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label_3 = QtGui.QLabel(unicode('节点属性' , 'gbk') , self.groupBox)
		self.label_3.setGeometry(QtCore.QRect(140, 10, 120, 20))
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label_4 = QtGui.QLabel(unicode('被驱动节点' , 'gbk') , self.groupBox)
		self.label_4.setGeometry(QtCore.QRect(270, 10, 120, 20))
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label_5 = QtGui.QLabel(unicode('被节点属性' , 'gbk') , self.groupBox)
		self.label_5.setGeometry(QtCore.QRect(400, 10, 120, 20))
		self.label_5.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label_6 = QtGui.QLabel(unicode('驱动类型:' , 'gbk') , self.layoutBox)
		self.label_6.setGeometry(QtCore.QRect(10, 310, 55, 20))

		self.label_7 = QtGui.QLabel(unicode('镜像替换:' , 'gbk') , self.layoutBox)
		self.label_7.setGeometry(QtCore.QRect(230, 310, 55, 20))
		
		self.label_7 = QtGui.QLabel('Search' , self.layoutBox)
		self.label_7.setGeometry(QtCore.QRect(300, 310, 50, 20))
				
		self.linetxt1 = QtGui.QLineEdit('L_' , self.layoutBox)
		self.linetxt1.setGeometry(QtCore.QRect(340, 310, 70, 20))
		
		self.label_7 = QtGui.QLabel('Replace' , self.layoutBox)
		self.label_7.setGeometry(QtCore.QRect(425, 310, 50, 20))	
			
		self.linetxt2 = QtGui.QLineEdit('R_' , self.layoutBox)
		self.linetxt2.setGeometry(QtCore.QRect(470, 310, 70, 20))
		
		self.radioButton_1 = QtGui.QRadioButton('x' , self.layoutBox)
		self.radioButton_1.setGeometry(QtCore.QRect(30, 340, 60, 20))
		
		self.radioButton_2 = QtGui.QRadioButton('y' , self.layoutBox)
		self.radioButton_2.setGeometry(QtCore.QRect(100, 340, 60, 20))
		
		self.radioButton_3 = QtGui.QRadioButton('z' , self.layoutBox)
		self.radioButton_3.setGeometry(QtCore.QRect(170, 340, 60, 20))
		
		self.comboBox = QtGui.QComboBox(self.layoutBox)
		self.comboBox.setGeometry(QtCore.QRect(70, 310, 90, 20))
		self.comboBox.addItem('Behavior')
		self.comboBox.addItem('Orientation')
		
		self.pushButton_2 = QtGui.QPushButton('Mirror' , self.layoutBox)
		self.pushButton_2.setGeometry(QtCore.QRect(10, 370, 530, 40))
		
		self.line = QtGui.QFrame(self.layoutBox)
		self.line.setGeometry(QtCore.QRect(10, 290, 530, 16))
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.label = QtGui.QLabel(unicode('获取驱动的父物体:' , 'gbk') , self.layoutBox)
		self.label.setGeometry(QtCore.QRect(10, 10, 90, 25))
		self.label.setMinimumSize(QtCore.QSize(0, 0))
		
		self.pushButton = QtGui.QPushButton(QtGui.QIcon(':zoomIn.png') , 'GET' , self.layoutBox)
		self.pushButton.setGeometry(QtCore.QRect(120, 10, 140, 25))
		
		
		self.setLayout(self.winlayout )
		
		self.makeConnections()
		self.initUiState()
		self.resize(560, 430)
	def flush(self):
		wins = getMayaWindow().findChildren(QtGui.QWidget , self.title) or []
		for c in wins:
			try:
				c.close()
			except:
				continue
			c.deleteLater()

	def makeConnections(self):
		self.comboBox.currentIndexChanged.connect(self.mirr_selectType)
		self.pushButton.clicked.connect(self.getDriverObject)
		self.listWidget.itemClicked.connect(self.setDriverAttr)
		self.listWidget_2.itemClicked.connect(self.getNodeWidget)
		self.listWidget_3.itemClicked.connect(self.getNodeAttrWidget)
		
		self.pushButton_2.clicked.connect(self.mirror_key)
		
	def initUiState(self):
		self.comboBox.setCurrentIndex(1)
		self.comboBox.setCurrentIndex(0)
		self.radioButton_1.setChecked(True)	
		
	def mirr_selectType(self , vaule):
		self.radioButton_1.setVisible(vaule)
		self.radioButton_2.setVisible(vaule)
		self.radioButton_3.setVisible(vaule)
	
	def setDriverAttr(self ,item = None,  *args):
		text = item.text()
		pm.select(text , r = True)
		
		self.listWidget_3.clearSelection()
		self.listWidget_4.clearSelection()
		self.listWidget_3.clear()
		self.listWidget_4.clear()
		
		listAttrs = []

		selObj = pm.PyNode(text)
		att = self.getDriverParentObjectAttr(selObj)
		listAttrs += att
		
		self.LoadingDit(listAttrs,self.listWidget_2)
	
	def mirror_key(self):
		attrItems = self.listWidget_2.selectedItems()
		if not attrItems:
			return OpenMaya.MGlobal_displayError('not select object attr')
		attr = attrItems[0].text()
		nodeName = self.listWidget.selectedItems()
		name = nodeName[0].text()
		
		self.mirrorSDK(name , attr)
		
	
	def getDriverObject(self):
		sel = pm.selected()
		listObject = [s.name() for s in sel if self.getDriverParentObjectAttr(s)]
		self.listWidget.clearSelection()
		self.listWidget_2.clearSelection()
		self.listWidget_3.clearSelection()
		self.listWidget_4.clearSelection()
		
		self.listWidget_2.clear()
		self.listWidget_3.clear()
		self.listWidget_4.clear()
		
		self.LoadingDit(listObject,self.listWidget)
	
	def LoadingDit(self , listObject = None , win = None):
		win.clear()
		for i in listObject:
			item = QtGui.QListWidgetItem(i)
			win.addItem(item)	
	
	def getDriverParentObjectAttr(self , node = None):
		attrLsit = []
		listAttribute = node.listAttr(k = True)
		for attribute in listAttribute:
			for ua in attribute.outputs(scn = True):
				if ua.nodeType() in ['animCurveUA' ,'animCurveUU','animCurveUL']:
					if attribute.attrName() not in attrLsit:
						attrLsit.append(attribute.attrName())
		
		return attrLsit

	def getNodeWidget(self , item = None):
		node = self.listWidget.selectedItems()[0].text()
		attr = self.listWidget_2.selectedItems()[0].text()
		
		nodeAttribute = pm.Attribute(node + '.' + attr)
		self.animCurveList = [ua for ua in nodeAttribute.outputs(scn = True) if ua.nodeType() in ['animCurveUA' ,'animCurveUU','animCurveUL'] ]
		nodeList = []
		self.nodeAttrDict = {}

		for uu in self.animCurveList:
			plugs = uu.outputs(p = True)
			for p in plugs:
				if p.node().name() not in nodeList:
					nodeList.append(p.node().name())
				if p.node().name() not in self.nodeAttrDict.keys():	
					self.nodeAttrDict[p.node().name()] = [p.attrName()]
				else:
					values = self.nodeAttrDict[p.node().name()]
					if p.attrName() not in values:
						self.nodeAttrDict.pop(p.node().name())
						values.append(p.attrName())
						self.nodeAttrDict[p.node().name()] = values
		
		self.LoadingDit(nodeList,self.listWidget_3)
	
	def getNodeAttrWidget(self , item = None):
		text = item.text()
		pm.select(text , r = True)
		attrList = self.nodeAttrDict[text]
		self.LoadingDit(attrList,self.listWidget_4)
	
	def mirrorSDK(self , node = None , attr = None , left = None , right = None):
		
		listAnimUA = self.animCurveList
		
		
		left =  self.linetxt1.text()
		right =  self.linetxt2.text()
		
		if node.find(left) == -1 :
			return OpenMaya.MGlobal_displayError('{0:s} : not is logogram {1:s} '.format(node , left))
		else:
			old = left
			new = right

		mirrorNode = node.replace(old , new)
		
		if not pm.objExists(mirrorNode):
			return OpenMaya.MGlobal_displayError(' not Exists {0:s} object'.format(mirrorNode))
		
		mirrorNodeAttr = pm.Attribute(mirrorNode + '.' + attr)
		
		for anim in listAnimUA:
			if pm.objExists(anim.replace(old , new)):
				pm.delete(anim.replace(old , new))
			copyAnim = pm.duplicate(anim , rr = True , n = anim.replace(old , new))[0]
			
			if not self.comboBox.currentIndex():
				if anim.nodeType() == 'animCurveUL':
					num = anim.numKeys()
					for i in range(num):
						value = anim.getValue(i)
						copyAnim.setValue(i, value*-1)
			
			elif self.comboBox.currentIndex():
				attrDict = {'translateX':1,'translateY':1,'translateZ':1,'rotateX':-1,'rotateY':-1,'rotateZ':-1}
				if self.radioButton_1.isChecked():
					attrDict['translateX'] = -1
					attrDict['rotateX'] = 1
				if self.radioButton_2.isChecked():
					attrDict['translateY'] = -1
					attrDict['rotateY'] = 1
				if self.radioButton_3.isChecked():
					attrDict['translateZ'] = -1
					attrDict['rotateZ'] = 1
					
				animList = self.getAnimEums(anim)
				
				output = anim.outputs(p = True)[0]
				attrName = output.attrName(longName=True)
				if attrName in attrDict.keys():
					for i in animList:
						i[1] = i[1]*attrDict[attrName]
				
				input = anim.inputs(p = True)[0]
				attrName = input.attrName(longName=True)
				if attrName in attrDict.keys():
					for i in animList:
						i[0] = i[0]*attrDict[attrName]
							
				animLists = sorted(animList , key = lambda x : x[0])
				for index , value in enumerate(animLists):
					pm.keyframe(copyAnim ,option = 'over' , index = index ,absolute =True , floatChange = value[0] , valueChange = value[1])	
						
			outPlug = anim.output.outputs(p = True)
		
			
			mirrorNodeAttr.connect(copyAnim.input , f = True)
			for plug in outPlug:
				name = self.mirrorNodeAttribute(plug , old , new)
				if pm.Attribute(name).isLocked():
					pm.Attribute(name).setLocked(0)
					copyAnim.output.connect(name , f = True)
					pm.Attribute(name).setLocked(1)
				else:
					copyAnim.output.connect(name , f = True)
		
		return OpenMaya.MGlobal_displayWarning('---------Driven Key Ok------------')
	
	def getAnimEums(self , node = None):
		
		if not node : return
		animList = []
		
		num = node.numKeys()
		for i in range(num):
			keyValue = pm.keyframe(node ,q = True , index = i , floatChange = True )[0]
			value =  pm.keyframe(node ,q = True , index = i , valueChange = True )[0]
			inType = node.getInTangentType(i).key
			outType =  node.getOutTangentType(i).key
			animIndex = [keyValue , value , inType , outType]
			animList.append(animIndex)
		
		return	animList
	
	def mirrorNodeAttribute(self , nodeAttribute = None , oldAttrbute = None , newAttrbute = None ):
		
		if not pm.objExists(nodeAttribute.node().replace(oldAttrbute , newAttrbute)):
			
			keyNode = self.getKeyObject(nodeAttribute.node())
			for k in keyNode:
				par = k.getParent()
				self.mirrorInterbedded(par , oldAttrbute , newAttrbute)
		
		mrNode = pm.PyNode(nodeAttribute.node().replace(oldAttrbute , newAttrbute))
		attrName = nodeAttribute.attrName()
		
		if not mrNode.hasAttr(attrName):
			
			
			if nodeAttribute.type() == 'enum':
				Enums = nodeAttribute.getEnums().items()
				addEnums = [key for key , value in Enums]
				mrNode.addAttr(attrName , at = nodeAttribute.type() , en = ':'.join(addEnums))
			
			else:
				mrNode.addAttr(attrName , at = nodeAttribute.type() , k = nodeAttribute.isKeyable())
				
				if 	nodeAttribute.type() != 'bool':
					if nodeAttribute.getMax():
						mrNode.setMax(nodeAttribute.getMax())
						
					if nodeAttribute.getMin():
						mrNode.setMin(nodeAttribute.getMin())
		
		attName = mrNode + '.' + attrName
		return attName
	
	def getKeyObject(self , objectNode = None):
		
		objectlistNode = []
		
		if objectNode.nodeType() != 'transform':
			objectlistNode.append(objectNode)
		else:
			if not objectNode.getShape():
				children = objectNode.getChildren()
				for c in children:
					objects = self.getKeyObject(c)
					objectlistNode += objects
			else:
				objectlistNode.append(objectNode)
		
		return objectlistNode
	
	
	def mirrorInterbedded(self , object = None , old = None , new = None):
		
		if object.nodeType() == 'transform' and not object.getShape():
			if not pm.objExists(object.replace(old , new)):
				children = [c.replace(old , new) for c in object.getChildren()]
				Cgroup = pm.group(children ,r = True , n = object.replace(old , new))
				pm.xform(Cgroup , os = True ,piv = [0,0,0] )
			parents = object.getParent()
			self.mirrorInterbedded(parents , old , new)





#def mirrorDrivenKey():	
if __name__=='__main__':
	a = MirrorDrivenKey()
	a.show()