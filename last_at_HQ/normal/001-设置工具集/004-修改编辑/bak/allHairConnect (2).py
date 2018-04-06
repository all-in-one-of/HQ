#!usr/bin/env python
#coding:utf-8
import pymel.core as pm 
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance
import functools


def getMayaWindow():
    """ pointer to the maya main window  
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr :
        return wrapInstance(long(ptr), QtGui.QMainWindow)


class AllHairConnect(QtGui.QDialog):
	
	def __init__(self , parent = getMayaWindow()):
		super(AllHairConnect , self).__init__(parent)
		self.main = None 
		self.char = None 
		
		self.QVBoxLayout = QtGui.QVBoxLayout()
		self.QVBoxLayout.setContentsMargins(5,5,5,5)
		
		self.GroupBox = QtGui.QGroupBox()
		self.QVBoxLayout.addWidget(self.GroupBox)
	
		self.qGroupBox = QtGui.QGroupBox(self.GroupBox)
		self.qGroupBox.setGeometry(QtCore.QRect(10, 10, 170, 60))
		#self.QVBoxLayout.addWidget(self.qGroupBox)
		
		self.qGrid1 = QtGui.QGridLayout()
		self.qGrid1.setContentsMargins(5,5,5,5)
		self.qGroupBox.setLayout(self.qGrid1)
		
		self.linetxt1 = QtGui.QLabel(unicode('ȷ��ë���㼶���淶����','gbk'))
		font1 = QtGui.QFont()
		font1.setPointSize(10)
		self.linetxt1.setFont(font1)
		self.linetxt1.setAlignment(QtCore.Qt.AlignCenter)
		self.linetxt1.setStyleSheet("color: rgb(255, 0, 0);")
		self.qGrid1.addWidget(self.linetxt1)
		
		self.linetxt2 = QtGui.QLabel(unicode('����ű����г���','gbk'))
		font2 = QtGui.QFont()
		font2.setPointSize(10)
		self.linetxt2.setFont(font2)
		self.linetxt2.setAlignment(QtCore.Qt.AlignCenter)
		self.linetxt2.setStyleSheet("color: rgb(255, 0, 0);")
		self.qGrid1.addWidget(self.linetxt2)
		
		self.qGroupBox1 = QtGui.QGroupBox(self.GroupBox)
		self.qGroupBox1.setGeometry(QtCore.QRect(10, 80, 170, 270))

		self.hiPushButton = QtGui.QPushButton('hi',self.qGroupBox1)
		self.hiPushButton.setGeometry(QtCore.QRect(10, 10, 150, 55))
		self.hiPushButton.setStyleSheet("font: 75 15pt \"Aharoni\";\ncolor: rgb(85, 255, 255);")

		self.PushButton = QtGui.QPushButton('hair',self.qGroupBox1)
		self.PushButton.setGeometry(QtCore.QRect(10, 75, 150, 55))
		self.PushButton.setToolTip(unicode('Լ��Ӱ���ߵ���','gbk'))
		self.PushButton.setStyleSheet("font: 75 15pt \"Aharoni\";\ncolor: rgb(85, 255, 255);")


		self.PushButton1 = QtGui.QPushButton('shave',self.qGroupBox1)
		self.PushButton1.setGeometry(QtCore.QRect(10, 140, 150, 55))
		self.PushButton1.setStyleSheet("font: 75 15pt \"Aharoni\";\ncolor: rgb(85, 255, 255);")
		
		
		self.PushButton2 = QtGui.QPushButton('yeti',self.qGroupBox1)
		self.PushButton2.setGeometry(QtCore.QRect(10, 205, 150, 55))
		self.PushButton2.setToolTip(unicode('Լ��yeti�ڵ�','gbk'))
		self.PushButton2.setStyleSheet("font: 75 15pt \"Aharoni\";\ncolor: rgb(85, 255, 255);")
		
		
		self.makeConnections()
		
		self.resize(200, 370)
		self.setMinimumSize(QtCore.QSize(200, 370))
		self.setMaximumSize(QtCore.QSize(200, 370))
		
		self.setWindowTitle("Hair Connect UI")
		self.setLayout(self.QVBoxLayout)
		self.initUiState()
		
	
	def makeConnections(self):
		self.PushButton.clicked.connect(self.hairLink)
		self.PushButton1.clicked.connect(self.shaveLink)
		self.PushButton2.clicked.connect(self.yetiLink)
		self.hiPushButton.clicked.connect(self.hiLink)

	def initUiState(self):
		
		pass

	def getGeoGroup(self):
		
		trans = pm.ls('*_geo*' , type = 'transform' )
		geoName = [ts for ts in trans if len(ts.getAllParents()) == 1]
		if not geoName:
			return None
		return geoName
	
	def allConnect(self):
		if not pm.objExists('Main') and not pm.objExists('Character'):
			OpenMaya.MGlobal_displayError('Not Main ctrl or Character ctrl')
			return
		self.main = pm.PyNode('Main')
		self.char = pm.PyNode('Character')
		
		if not self.main.hasAttr('showMod'):
			self.main.addAttr('showMod' , at = 'long' , min= 0 , max = 1 , dv = 1 , k = True)
		
		geo = self.getGeoGroup()
		if geo:
			if geo[0] not in self.main.showMod.outputs():
				self.main.showMod.connect(geo[0].v , f = True)
		#self.hairLink()
		#self.shaveLink()
		#self.yetiLink()
		
	def hiLink(self):
		'''
		
		'''
		self.allConnect()
			
	
	def hairLink(self):	
		'''
		examine hair 
		'''	
		self.allConnect()
		
		hairNodeList = pm.ls(type = 'hairSystem')	
		if hairNodeList:
			if not pm.objExists('hair_G') :
				OpenMaya.MGlobal_displayError('Not hair_G Group')
				return
			if not pm.objExists('hair_setup_G'):
				OpenMaya.MGlobal_displayError('Not hair_setup_G Group')
				return
			if not pm.objExists('hair_show_G'):
				OpenMaya.MGlobal_displayError('Not hair_show_G Group')
				return
			
			hairGroup = pm.PyNode('hair_G')
			if self.main.showMod not in hairGroup.v.inputs(p = True):
				self.main.showMod.connect(hairGroup.v , f = True)
			
			if not self.main.hasAttr('hair'):
				self.main.addAttr('hair' , at = 'long' ,min= 0 , max = 1 , dv = 0 , k = True)
			
			if pm.PyNode('hair_show_G') not in self.main.hair.outputs():
				self.main.hair.connect('hair_show_G.v' , f = True)
			
			for hair in hairNodeList:
				hair.simulationMethod.set(1)
				
			hairNameList = [n.name() for n in hairNodeList]
			OpenMaya.MGlobal_displayInfo('%s All attribute simulationMethod revamp Stactic'%hairNameList)	
			
			nucleusNodeList = pm.ls(type = 'nucleus')
			if nucleusNodeList:
				for nucleus in nucleusNodeList:
					nucleus.enable.set(0)
					
				OpenMaya.MGlobal_displayInfo('%s All attribute enable revamp 0'%nucleusNodeList)
			
			self.displayDialog('hairSystem����ΪStatic״̬�� ������Enable�ѹص���')				
		else:
			return	False	
	
	def shaveLink(self):
		'''
		examine shave
		'''	
		self.allConnect()
					
		if 'shaveHair' in pm.allNodeTypes():
			shaveNodeList = pm.ls(type = 'shaveHair')
			
			if shaveNodeList:
				if not pm.objExists('shave_G'):
					OpenMaya.MGlobal_displayError('Not shave_G Group')
					return
				if not pm.objExists('shave_setup_G'):
					OpenMaya.MGlobal_displayError('Not shave_setup_G Group')
					return
				if not pm.objExists('shave_show_G'):
					OpenMaya.MGlobal_displayError('Not hair_show_G Group')
					return	
												
				shaveGroup = pm.PyNode('shave_G')
				if self.main.showMod not in shaveGroup.v.inputs(p = True):
					self.main.showMod.connect(shaveGroup.v , f = True)
					
				if not self.main.hasAttr('shave'):
					self.main.addAttr('shave' , at = 'long' ,min= 0 , max = 1 , dv = 0 , k = True)
				
				if pm.PyNode('shave_show_G') not in self.main.shave.outputs():
					self.main.shave.connect('shave_show_G.v' , f = True)
				
				for shave in shaveNodeList:
					shaveAttrs = ['.scale' , '.rootThickness' , '.tipThickness' , '.displacement' , '.rootSplay' , '.tipSplay']
					shaveAttrsList = [shave+att for att in shaveAttrs]
					map(self.scaleLink ,shaveAttrsList)
					OpenMaya.MGlobal_displayInfo('Character connected %s'%shave)
					
				self.setMesh('shaveHair')
				self.displayDialog('shave�ڵ��ѹ����ܿص��������ԣ� ��Ƥģ�������ò�����Ⱦ�� ������������')	
		else:
			return False
	
	def yetiLink(self):	
		'''
		examine yeti
		'''
		self.allConnect()
		
		if 'pgYetiMaya' in pm.allNodeTypes():
			yetiNodeList = pm.ls(type = 'pgYetiMaya')
			yetiList = [node.getParent() for node in yetiNodeList]
			if yetiList:
				if not pm.objExists('yeti_G'):
					OpenMaya.MGlobal_displayError('Not yeti_G Group')
					return
				if not pm.objExists('yeti_setup_G'):
					OpenMaya.MGlobal_displayError('Not yeti_setup_G Group')
					return
				
				yetiGroup = pm.PyNode('yeti_G')
				if self.main.showMod not in yetiGroup.v.inputs(p = True):
					self.main.showMod.connect(yetiGroup.v , f = True)	
					
				if not self.main.hasAttr('yeti'):
					self.main.addAttr('yeti' , at = 'long' ,min= 0 , max = 1 , dv = 0 , k = True)
				
				if pm.PyNode('yeti_show_G') not in self.main.yeti.outputs():
					self.main.yeti.connect('yeti_show_G.v' , f = True)	
																		
				conAttrList = []
				
				for shape in yetiNodeList:
					if shape.cacheFileName.get():
						yeti = shape.getParent() 
						cons = yeti.listRelatives(type = 'parentConstraint')
						
						if not cons:
							OpenMaya.MGlobal_displayError('Not do %s node parentConstraint'%yeti)
						else:	
							conAttrs = [attr.listAttr(ud = True)[0] for attr in cons]
						
							conAttrList += conAttrs
						
						if not self.main.hasAttr('abc'):
							self.main.addAttr('abc' , at = 'enum' , en = "efx:anim:" , k = True)
							self.main.abc.set(1)
							
						if self.main.abc not in shape.fileMode.inputs(p = True):
							self.main.abc.connect(shape.fileMode , f = True)
						
				if conAttrList:
					for att in conAttrList:
						if self.main.abc not in att.inputs(p = True):
							self.main.abc.connect( att , f = True)
				
				self.setMesh('pgYetiMaya')
				
				if conAttrList:
					self.displayDialog('�ܿ�abc�����ѹ���yeti��Լ���ڵ��cache���ԣ� ��Ƥģ�������ò�����Ⱦ�� ������������')
				else:
					self.displayDialog('�ܿ�abc�����ѹ���yeti��cache���ԣ� ��Ƥģ�������ò�����Ⱦ�� ������������ Լ���ڵ�û�У�')
		else:
			return False
	
	def scaleLink(self , nodeAttr = None ):
		'''
		@attr : str 
		'''
		attrValue = pm.getAttr(nodeAttr)
		if not pm.objExists(nodeAttr.replace('.' , '_') + '_MD'):
			attrMD = pm.createNode('multiplyDivide' , name = nodeAttr.replace('.' , '_') + '_MD')
		else:
			attrMD = pm.PyNode(nodeAttr.replace('.' , '_') + '_MD')
			
		attrMD.input2X.set(attrValue)
		
		if self.char.sx not in attrMD.input1X.inputs(p = True):
			self.char.sx.connect(attrMD.input1X , f = True)
			
		pulgs = pm.listConnections(nodeAttr , s = True , d = False , p = True)
		if attrMD.outputX not in pulgs:
			attrMD.outputX.connect(nodeAttr , f = True)
		
		return attrMD
		
	
	def displayDialog(self , txet = None):
		'''
		@text : str , This is the text is error result
		'''
		window = pm.window( title="outcome display" , iconName='Short Name' , widthHeight=(200, 70) )
		pm.columnLayout( adjustableColumn=True )
		cmds.text('')
		txetList = txet.split(' ')
		for s in txetList:
			cmds.text( label=s, align='center' )
		pm.setParent( '..' )
		pm.showWindow( window )
		
		
	
	def setRender(self , shape = None , value = False):
		'''
		@shape : str , This is the shape is shape name 
		@value : bool , True or False
		'''
		attr = ['.castsShadows' , '.receiveShadows' , '.motionBlur' , '.smoothShading' , '.primaryVisibility' , '.visibleInReflections' , '.visibleInRefractions' , '.doubleSided']
		
		for atr in attr:
			pm.setAttr(shape + atr  , value)
	
	
	def setMesh(self , nodeType1 = None):
		'''
		@groupName : str , This is the grpup name
		'''
		if not nodeType1:
			return 
		if nodeType1 == 'shaveHair':
			mesh = pm.ls(type = 'shaveHair' )
			meshShape = []
			for s in mesh:
				in1 = s.displayNode.inputs(sh = True)[0]
				in2 = s.inputMesh[0].inputs(sh = True)[0]
				if not in1:
					OpenMaya.MGlobal_displayError('shaveHair not %s mesh '%in1)
				if not in2:
					OpenMaya.MGlobal_displayError('shaveHair not %s ski mesh '%in2)
				meshShape.append(in1)
				meshShape.append(in2)
		
		if nodeType1 == 'pgYetiMaya':
			mesh = pm.ls(type = 'pgYetiMaya' )
			meshShape = []
			for s in mesh:
				in1 = s.inputGeometry[0].inputs(sh = True)[0]
				in2 = s.inputGeometry[1].inputs(sh = True)[0]
				if not in1:
					OpenMaya.MGlobal_displayError('pgYetiMaya not %s mesh '%in1)
				if not in2:
					OpenMaya.MGlobal_displayError('pgYetiMaya not %s reference mesh '%in2)	
					
				meshShape.append(in1)
				meshShape.append(in2)		

		for shape in meshShape:
			if not shape.getParent().v.get(l = True ):
				shape.getParent().v.set(0 , l = True , k = False , cb = True)
			self.setRender(shape.name())
		



hairs = AllHairConnect()
hairs.show()


