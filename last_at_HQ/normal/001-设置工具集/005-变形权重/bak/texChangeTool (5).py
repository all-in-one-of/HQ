import pymel.core as pm 
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance
import re
import functools


def getMayaWindow():

	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr:
		return wrapInstance(long(ptr) , QtGui.QMainWindow)


class AnamorphosisLinkUI(QtGui.QDialog):

	def __init__(self , ctrName = None , nodeName = None, parent = getMayaWindow()):
		super(AnamorphosisLinkUI , self).__init__(parent)
		self.colorMapDict = {0:[(0,0,0) , 1.0], 
							1:[(255,255,255),0.9], 
							2:[(255,0,0) , 0.00],
							3:[(0,255,0) , 0.30],
							4:[(0,0,255) , 0.65],
							5:[(255,255,0) , 0.15],
							6:[(255,108,49) , 0.10],
							7:[(5,220,255) , 0.50],
							8:[(200,0,200) , 0.85],
							9:[(72,72,72) , 0.283],
							10:[(171,171,171) , 0.671]}
		
		self.ctrName = ctrName 
		self.nodeName = nodeName
		self.geoName = None
		
		self.resize(460, 300)
		
		self.tabWidget = QtGui.QTabWidget(self)
		self.tabWidget.setGeometry(self.geometry())
		self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
		self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
		self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
		self.tabWidget.setMovable(False)
		self.tabWidget.setStyleSheet('background-color: rgb(68, 68, 68);')
		
		self.tab_1 = QtGui.QWidget()
		self.tabWidget.addTab(self.tab_1, 'Hi File')
		#self.tab_1.setStyleSheet('color: rgb(0, 181, 0);')
		
		#self.hiLine = Splitter('Hi File' ,self.tab)
		#self.hiLine.setGeometry(QtCore.QRect(5, 5, 460, 20))
		
		self.hiGroupBox = QtGui.QGroupBox('Get Control And SG Node Name' , self.tab_1)
		self.hiGroupBox.setGeometry(QtCore.QRect(5, 5, 450, 260))
		
		self.stlabel = QtGui.QLabel('Automatic Access To The Node :' , self.hiGroupBox)
		self.stlabel.setGeometry(QtCore.QRect(10, 20, 170, 20))
		self.stlabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.stlabel.setStyleSheet('color: rgb(255, 0, 0);')
		
		self.stButton = QtGui.QPushButton('Get All SG' , self.hiGroupBox)
		self.stButton.setGeometry(QtCore.QRect(190, 20, 80, 20))
		self.stButton.setStyleSheet('color: rgb(255, 0, 0);\nbackground-color: rgb(255, 255, 0);')
		
		self.hiLine = Splitter('Below So' ,self.hiGroupBox)
		self.hiLine.setGeometry(QtCore.QRect(5, 40, 440, 20))
		
		self.qGroupBox = QtGui.QGroupBox(self.hiGroupBox)
		self.qGroupBox.setGeometry(QtCore.QRect(5, 65, 440, 100))
		
		self.label1 = QtGui.QLabel('Control Name' , self.qGroupBox)
		self.label1.setGeometry(QtCore.QRect(5, 10, 70, 20))
		self.label1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.linetxt1 = QtGui.QLineEdit(self.qGroupBox)
		self.linetxt1.setGeometry(QtCore.QRect(85, 10, 60, 20))
		self.linetxt1.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.PushButton1 = QtGui.QPushButton('Get' , self.qGroupBox)
		self.PushButton1.setGeometry(QtCore.QRect(155, 10, 50, 20))
		self.PushButton1.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.comBox = QtGui.QComboBox(self.qGroupBox)
		self.comBox.setGeometry(QtCore.QRect(375, 10, 60, 20))
		self.comBox.setStyleSheet('background-color: rgb(98, 98, 98);')

		self.label1add = QtGui.QLabel('Attribute' , self.qGroupBox)
		self.label1add.setGeometry(QtCore.QRect(215, 10, 50, 20))
		self.label1add.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		self.comBoxAdd = QtGui.QComboBox(self.qGroupBox)
		self.comBoxAdd.setGeometry(QtCore.QRect(275, 10, 90, 20))
		self.comBoxAdd.setStyleSheet('background-color: rgb(98, 98, 98);')


		self.labelm = QtGui.QLabel('Tou Geo Name' , self.qGroupBox)
		self.labelm.setGeometry(QtCore.QRect(5, 40 , 80, 20))
		self.labelm.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.linetxtm = QtGui.QLineEdit(self.qGroupBox)
		self.linetxtm.setGeometry(QtCore.QRect(95, 40, 180, 20))
		self.linetxtm.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.PushButtonm = QtGui.QPushButton('Get' , self.qGroupBox)
		self.PushButtonm.setGeometry(QtCore.QRect(285, 40, 50, 20))
		self.PushButtonm.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.label2 = QtGui.QLabel('SG Node Name' , self.qGroupBox)
		self.label2.setGeometry(QtCore.QRect(5, 70 , 80, 20))
		self.label2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.linetxt2 = QtGui.QLineEdit(self.qGroupBox)
		self.linetxt2.setGeometry(QtCore.QRect(95, 70, 180, 20))
		self.linetxt2.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.PushButton2 = QtGui.QPushButton('Get' , self.qGroupBox )
		self.PushButton2.setGeometry(QtCore.QRect(285, 70, 50, 20))
		self.PushButton2.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.linetxt3 = QtGui.QLineEdit(self.qGroupBox)
		self.linetxt3.setGeometry(QtCore.QRect(345, 70, 90, 20))
		self.linetxt3.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.line1 = Splitter(parent = self.hiGroupBox , shadow=False, color=(60,60,60))
		self.line1.setGeometry(QtCore.QRect(40, 165, 370, 20))
		
		self.gropWid = QtGui.QWidget(self.hiGroupBox)
		self.gropWid.setGeometry(QtCore.QRect(5, 180, 440, 30))
		
		self.qGrid2 = QtGui.QGridLayout(self.gropWid)
		self.qGrid2.setContentsMargins(4,2,4,2)
		
		self.colotButtonList = [self.colotButton(i , self.qGrid2) for i in range(11)]
		
		self.okButton = QtGui.QPushButton('Set Driven Keyframe' ,self.hiGroupBox )
		self.okButton.setGeometry(QtCore.QRect(5, 220, 440, 30))
		self.okButton.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		
		self.tab_2 = QtGui.QWidget()
		self.tabWidget.addTab(self.tab_2, 'Low File')
		#self.tab_2.setStyleSheet('color: rgb(0, 181, 0);')
		
		sTex1 = QtGui.QLabel('Method :' , self.tab_2)
		sTex1.setGeometry(QtCore.QRect(5, 5, 450, 20))
		sTex1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		
		sTex2 = QtGui.QLabel('1. Open Low File' , self.tab_2)
		sTex2.setGeometry(QtCore.QRect(5, 30, 450, 20))
		sTex2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		
		sTex3 = QtGui.QLabel('2. Reference Hi file ' , self.tab_2)
		sTex3.setGeometry(QtCore.QRect(5, 55, 450, 20))
		sTex3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		
		self.lowGroupBox = QtGui.QGroupBox('Reference Hi File' , self.tab_2)
		self.lowGroupBox.setGeometry(QtCore.QRect(5, 85, 450, 160))
		
		
		self.label = QtGui.QLabel('Low Control :' , self.lowGroupBox)
		self.label.setGeometry(QtCore.QRect(10, 20, 80, 20))
		self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.lineEdit = QtGui.QLineEdit(self.lowGroupBox)
		self.lineEdit.setGeometry(QtCore.QRect(100, 20, 231, 20))
		self.lineEdit.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.pushButton = QtGui.QPushButton('Get' , self.lowGroupBox)
		self.pushButton.setGeometry(QtCore.QRect(350, 20, 81, 20))
		self.pushButton.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.label_2 = QtGui.QLabel('Hi Mesh :' , self.lowGroupBox)
		self.label_2.setGeometry(QtCore.QRect(10, 50, 80, 20))
		self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.lineEdit_2 = QtGui.QLineEdit(self.lowGroupBox)
		self.lineEdit_2.setGeometry(QtCore.QRect(100, 50, 231, 20))
		self.lineEdit_2.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.pushButton_2 = QtGui.QPushButton('Get' , self.lowGroupBox)
		self.pushButton_2.setGeometry(QtCore.QRect(350, 50, 81, 23))
		self.pushButton_2.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.label_3 = QtGui.QLabel('Low Mesh :' , self.lowGroupBox)
		self.label_3.setGeometry(QtCore.QRect(10, 80, 80, 20))
		self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
		
		self.lineEdit_3 = QtGui.QLineEdit(self.lowGroupBox)
		self.lineEdit_3.setGeometry(QtCore.QRect(100, 80, 231, 20))
		self.lineEdit_3.setStyleSheet('background-color: rgb(42, 42, 42);')
		
		self.pushButton_3 = QtGui.QPushButton('Get' , self.lowGroupBox)
		self.pushButton_3.setGeometry(QtCore.QRect(350, 80, 81, 23))
		self.pushButton_3.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		self.line = QtGui.QFrame(self.lowGroupBox)
		self.line.setGeometry(QtCore.QRect(10, 100, 431, 20))
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		
		self.pushButton_4 = QtGui.QPushButton('Transfer' , self.lowGroupBox)
		self.pushButton_4.setGeometry(QtCore.QRect(10, 120, 431, 30))
		self.pushButton_4.setStyleSheet('background-color: rgb(98, 98, 98);')
		
		
		self.makeConnections()
		self.setWindowTitle("SG Node UI")
		
		
		self.setMinimumSize(QtCore.QSize(460, 300))
		self.setMaximumSize(QtCore.QSize(460, 300))
		self.initUiState()
		self.show()

	def colotButton(self, tetx = None ,parentLayout = None):
		colorbtn1 = QtGui.QPushButton(str(tetx))
		colorbtn1.setMinimumSize(0,0)
		colorbtn1.setMaximumSize(40,40)
		colorbtn1.setCheckable(True)
		bColor = self.colorMapDict.get(tetx)[0]
		colorbtn1.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white;}' % (bColor[0],bColor[1],bColor[2]))
		parentLayout.addWidget(colorbtn1,0,tetx)
		return colorbtn1
		
	
	def makeConnections(self):
		self.PushButton1.clicked.connect(self.setTxt1)
		self.PushButton2.clicked.connect(self.setTxt2)
		self.PushButtonm.clicked.connect(self.setTxtm)
		self.okButton.clicked.connect(self.sg_connectAttr)
		self.comBox.activated.connect(self.setBox1)
		self.stButton.clicked.connect(self.getAllSG)
		
		self.comBoxAdd.activated.connect(self.getAeoAndSG)
		
		self.pushButton.clicked.connect(self.setTxt_1)
		self.pushButton_2.clicked.connect(self.setTxt_2)
		self.pushButton_3.clicked.connect(self.setTxt_3)
		self.pushButton_4.clicked.connect(self.copyConnect)
		
		for ide,bn in enumerate(self.colotButtonList):
			bn.clicked.connect(functools.partial(self.setColor1 , ide))
			#bn.clicked.connect(bn.pressed)
	
	def initUiState(self):
		self.linetxt1.setText(str(self.ctrName))
		self.linetxt1.setEnabled(False)
		self.linetxt2.setText(str(self.nodeName))
		self.linetxt2.setEnabled(False)
		self.linetxtm.setText(str(self.geoName))
		self.linetxtm.setEnabled(False)
		self.linetxt3.setEnabled(False)
		
		self.lineEdit.setEnabled(False)
		self.lineEdit_2.setEnabled(False)
		self.lineEdit_3.setEnabled(False)
		
		self.getCtrLAttrList()
		
	
	def setColor1(self ,color1 = None):
		node = pm.PyNode(self.nodeName)
		if node.hasAttr('color'):
			self.linetxt3.setText(str(self.colorMapDict.get(color1)[1]))
			node.hue[0].hue_FloatValue.set(self.colorMapDict.get(color1)[1])
			node.color.set([a/255.0 for a in self.colorMapDict.get(color1)[0]])

	def setBox1(self):
		txt1 = self.comBoxAdd.currentText()
		txt2 = self.comBox.currentIndex()
		main = pm.Attribute(self.ctrName+'.'+txt1)
		main.set(int(txt2))
					
	
	def setTxt1(self):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		self.ctrName = ctrName
		self.linetxt1.setText(str(self.ctrName))
		if self.linetxt1.text() != 'None':
			self.getCtrLAttributeList()
			
	def setTxtm(self):
		geoName = self.sg_selectName()
		if not geoName:
			OpenMaya.MGlobal_displayError('not select tou object , please again select')
			return
		self.geoName = geoName
		self.linetxtm.setText(str(self.geoName))
		
	def setTxt2(self):
		nodeName = self.sg_selectName()
		if not nodeName:
			OpenMaya.MGlobal_displayError('not select remapHsv , please again select')
			return 
		self.nodeName = nodeName
		if pm.PyNode(self.nodeName).type() == 'remapHsv':
			self.linetxt2.setText(str(self.nodeName))
			OpenMaya.MGlobal_displayInfo('<<<<<<<< Load Ok >>>>>>>>')
		else:
			OpenMaya.MGlobal_displayWarning('Select object not is remapHsv node ,%s is %s type'%(self.nodeName , pm.PyNode(self.nodeName).type()))
			return
	
	def sg_connectAttr(self):
		main = pm.PyNode(self.ctrName)
		rbg = pm.PyNode(self.nodeName)
		
		if not self.geoName:
			OpenMaya.MGlobal_displayError('not select tou object , please again select')
			return 
		geo = pm.PyNode(self.geoName)
		
		self.linkeAttr(main , geo , rbg )
		
		
		rbg.hue[0].hue_FloatValue.set(float(self.linetxt3.text()))
		if rbg.hasAttribute('fileTextureName'):
			pm.setDrivenKeyframe(rbg.hue[0].hue_FloatValue , currentDriver = rbg.fileTextureName , itt = 'linear' , ott = 'linear')
			pm.setDrivenKeyframe(rbg.color , currentDriver = rbg.fileTextureName , itt = 'linear' , ott = 'linear')
			OpenMaya.MGlobal_displayInfo('------ add setKey OK -----')
		else :
			OpenMaya.MGlobal_displayError('remapHsv node not fileTextureName attribute')
			return 
		
		
	def linkeAttr(self,main = None ,geo = None , rbg = None  ):
		txt = self.comBoxAdd.currentText()
		mainAttr = pm.Attribute(self.ctrName+'.'+txt)
		
		if not geo.hasAttr('fileTextureName'):
			emDirt = mainAttr.getEnums()
			enDirtKey = emDirt.keys()
			enstr = ':'.join(enDirtKey)
			geo.addAttr('fileTextureName' , at = 'enum' , en = enstr , k = True)
			
		if mainAttr not in geo.fileTextureName.inputs(p = True):
			mainAttr.connect(geo.fileTextureName , f = True)
			
		if not rbg.hasAttr('fileTextureName'):
			emDirt = mainAttr.getEnums()
			enDirtKey = emDirt.keys()
			self.hsvAddAttr(rbg , enDirtKey)
				
		if geo.fileTextureName not in rbg.fileTextureName.inputs(p = True):
			geo.fileTextureName.connect(rbg.fileTextureName , f = True)
		
		if pm.ls(type = 'choice'):
			pat = [a for a in pm.ls(type = 'choice') if a.outputs(type= 'choice')]
			if pat:
				if rbg.fileTextureName not in pat[0].selector.inputs(p = True):
					rbg.fileTextureName.connect(pat[0].selector , f = True)
		else:
			if not pm.ls(type ='alSwitchColor'):
				return OpenMaya.MGlobal_displayError('Not choice and alSwitchColor type')
			pat = [a for a in pm.ls(type ='alSwitchColor') if a.mix.outputs(type= 'alSwitchColor')]
			if pat:
				if rbg.fileTextureName not in pat[0].mix.inputs(p = True):
					rbg.fileTextureName.connect(pat[0].mix , f = True)
		
		
	def sg_selectName(self):
		sel = pm.ls(sl=True)
		if sel:
			s = sel[0].name()
			return s
		else:
			return None
			
	def getCtrLAttributeList(self):
		if self.ctrName :
			main = pm.PyNode(self.ctrName)
			listAttribute = [attr.attrName() for attr in main.listAttr(ud = True) if attr.get(type = True) == 'enum' if attr.attrName() not in ['abc']]
			if not listAttribute:
				return OpenMaya.MGlobal_displayWarning('Select ctrl not is fileTextureName attribute , Again select .....')
			self.comBoxAdd.clear()
			self.comBoxAdd.addItems(listAttribute)
			self.getCtrLAttrList()
			self.getAeoAndSG()
			
	def getAeoAndSG(self):	
		txt = self.comBoxAdd.currentText()
		mainAttr = pm.Attribute(self.ctrName+'.'+txt)
		geo = mainAttr.outputs(p = True)
		if geo:
			if geo[0].node().nodeType() == 'transform':
				self.geoName = geo[0].node().name()
				self.linetxtm.setText(self.geoName)
				rbg = geo[0].outputs(p = True)
				if rbg :
					self.nodeName = rbg[0].node().name()
					self.linetxt2.setText(self.nodeName)
			
	
	def getCtrLAttrList(self):	
		txt = self.comBoxAdd.currentText()
		if self.ctrName :
			emDirt = pm.Attribute(self.ctrName+'.'+txt).getEnums()
			enDirtKey = emDirt.keys()
			self.comBox.clear()
			self.comBox.addItems(enDirtKey)
			OpenMaya.MGlobal_displayInfo('<<<<<<<< Load Ok >>>>>>>>')
		
					
	def getAllSG(self):
		tex = TexChangeTool()
		tex.texlink()
		self.linetxt1.setText(str(tex.main))
		self.linetxt2.setText(str(tex.rgbNode))
		
		self.ctrName = tex.main
		self.nodeName = tex.rgbNode
		self.getCtrLAttributeList()
		
	
	
	def setTxt_1(self):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		self.ctrName = ctrName
		self.lineEdit.setText(str(self.ctrName))

			
	def setTxt_2(self):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		self.ctrName = ctrName
		self.lineEdit_2.setText(str(self.ctrName))


	def setTxt_3(self):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		self.ctrName = ctrName
		self.lineEdit_3.setText(str(self.ctrName))

	def getShaderNode(self, mesh = None):
		if mesh.nodeType() == 'mesh':
			displayShader = mesh.instObjGroups.outputs()
			colorNode = displayShader[0].surfaceShader.inputs()
			return colorNode[0]
		else:
			return  OpenMaya.MGlobal_displayError('{:s} type is not mesh '.format(mesh))
	
	def getColorKeyNode(self , shaderNode = None):
		HSV_Node = shaderNode.hardwareColor.inputs()
		if not HSV_Node:
			return OpenMaya.MGlobal_displayError('Not HSV Node')
		addAttrNode = HSV_Node[0].listAttr(ud = True)
		listAnimUU = [uu for uu in addAttrNode[0].outputs() if uu.nodeType() == 'animCurveUU']
		return self.createNodeConnect(HSV_Node[0] , addAttrNode[0] , listAnimUU)
		
	def createNodeConnect(self , hsv = None , attrNode = None , listNode = None):
		copyHsv = pm.duplicate(hsv , rr = True)[0]
		attrName = attrNode.attrName(longName = True)
		for i in listNode:
			copyRBG = pm.duplicate(i , rr = True)[0]
			pm.connectAttr(copyHsv +'.' +attrName , copyRBG.input ,f = True)
			outputs = i.outputs(p =True)
			for p in outputs:
				copyRBG.output.connect(p.name().replace(hsv.name() , copyHsv.name()) , f = True)
		return copyHsv 
		
	def copyConnect(self):
		if self.lineEdit_2.text():
			sm = pm.PyNode(self.lineEdit_2.text()).getShape()
		else :
			return OpenMaya.MGlobal_displayError('not select object')
		
		if self.lineEdit_3.text():
			em = pm.PyNode(self.lineEdit_3.text()).getShape()
		else :
			return OpenMaya.MGlobal_displayError('not select object')
		
		if self.lineEdit.text():
			main = pm.PyNode(self.lineEdit.text())
		else :
			return OpenMaya.MGlobal_displayError('not select object')		
		
		
		st = self.getShaderNode(sm)
		en = self.getShaderNode(em)
		
		
		cpHsv = self.getColorKeyNode(st)
		
		if cpHsv:
			attr = cpHsv.listAttr(ud = True)[0]
		else :
			return penMaya.MGlobal_displayError('Not HSV Node')
		
		name = attr.attrName(longName = True)
		key = attr.getEnums().keys()
		
		if main.hasAttr(name):
			return OpenMaya.MGlobal_displayWarning('Already Execute')
		
		if not main.hasAttr(name):
			main.addAttr(name , at = 'enum' , en = ':'.join(key) , k = True)
		
		pm.connectAttr(main+'.'+name , cpHsv+'.'+name , f = True)
		cpHsv.outColor.connect(en.hardwareColor , f = True)
		
		return OpenMaya.MGlobal_displayInfo('Execute Ok')

	
	def hsvAddAttr(self , node = None , attr = None):
		if isinstance(attr , list):
			mFnAttr = OpenMaya.MFnEnumAttribute()
			inRadius = mFnAttr.create('fileTextureName' , 'ftn' )
			for it,at in enumerate(attr):
				mFnAttr.addField(at , it)
			mFnAttr.setReadable(1)
			mFnAttr.setWritable(1)
			mFnAttr.setStorable(1)
			mFnAttr.setKeyable(1)		
			node.addAttribute(inRadius)

				
class TexChangeTool(object):
	def __init__(self):
		self.main =  None
		self.rgbNode = None	
		
		self.attrList = list('abcdefghijk')
		
		self.alColorDict ={0:(0.0, 0.0, 0.0),
							1:(1.0, 1.0, 1.0),
							2:(1.0, 0.0, 0.0),
							3:(0.0, 1.0, 0.0),
							4:(0.0, 0.0, 1.0),
							5:(1.0, 1.0, 0.0),
							6:(1.0, 0.0, 1.0),
							7:(0.0, 1.0, 1.0)}
	
	
	def texlink(self):
		if pm.objExists('Main'):
			self.main = pm.PyNode('Main') 
		else:
			OpenMaya.MGlobal_displayError('not Main ctrl')
			return
		
		if 'choice' in pm.allNodeTypes():
			all = pm.ls(type = 'choice')
			if all:
				if len(all) == 1:
					pat = all[0]
				else:
					pat = [a for a in all if a.outputs(type= 'choice')][0]
					
				self.linksType(pat , 0)
			elif pm.ls(type = 'alSwitchColor'):
				pat = [a for a in pm.ls(type ='alSwitchColor') if a.mix.outputs(type= 'alSwitchColor')]
				if not pat:
					OpenMaya.MGlobal_displayWarning('not choice and alSwitchColor Node')
				
				self.linksType(pat[0] , 1)
			else:
				OpenMaya.MGlobal_displayWarning('not choice Node')
				return
		else:
			OpenMaya.MGlobal_displayWarning('Thes is file not anamorphosis')
			return	
		ctrName = self.main.name()
		try:
		    rgbName = 	self.rgbNode.name()	
		except:
		    rgbName = None
		    OpenMaya.MGlobal_displayWarning('not select RGB Node')
		    
	def linksType(self , node = None , nodeInt = 0):
		
		if nodeInt == 0:
			file1 = node.input.inputs()
			num =[self.attrList[i] for i in range(len(file1))]
		
		if nodeInt == 1:
			alAttr = ['inputA' , 'inputB' , 'inputC' , 'inputD' , 'inputE' , 'inputF' , 'inputG' , 'inputH']
			file1 = [value for indxe , value in enumerate(alAttr) if pm.getAttr(node+'.'+ value) != self.alColorDict[indxe]]
			num =[self.attrList[i] for i in range(len(file1))]

		
		enstr = ':'.join(num)
		if self.main.hasAttr('tex'):
			self.main.deleteAttr('tex')
				
		if not self.main.hasAttr('fileTextureName'):
			self.main.addAttr('fileTextureName' , at = 'enum' , en = enstr , k = True)
		
		self.rgbNode = self.getSG()
		self.deleConnect(self.rgbNode)
		
		if not self.rgbNode.hasAttribute('fileTextureName'):
			self.hsvAddAttr(self.rgbNode , num)
		
		if nodeInt == 0:
			if self.rgbNode.fileTextureName not in node.selector.inputs(p = True):
				self.rgbNode.fileTextureName.connect(node.selector , f = True)
		
		if nodeInt == 1:
			if self.rgbNode.fileTextureName not in node.mix.inputs(p = True):
				self.rgbNode.fileTextureName.connect(node.mix , f = True)
		
		if not self.rgbNode.fileTextureName.inputs():
			self.main.fileTextureName.connect(self.rgbNode.fileTextureName ,f = True)	    
		
		
				
	def hsvAddAttr(self , node = None , attr = None):
		if isinstance(attr , list):
			mFnAttr = OpenMaya.MFnEnumAttribute()
			inRadius = mFnAttr.create('fileTextureName' , 'ftn' )
			for it,at in enumerate(attr):
				mFnAttr.addField(at , it)
			mFnAttr.setReadable(1)
			mFnAttr.setWritable(1)
			mFnAttr.setStorable(1)
			mFnAttr.setKeyable(1)		
			node.addAttribute(inRadius)
	
										
	def getSG(self):
		allHsv = pm.ls(type = 'remapHsv')
		if not allHsv:
			OpenMaya.MGlobal_displayError('not remapHsv Node')
		if len(allHsv) == 1:
			return allHsv[0]
		else :
			for hsv in allHsv :
				out = hsv.outputs(p = True)
				comp = re.compile('.+hardwareColor')
				for i in out:
					if comp.match(i.name()):
						return hsv
				
	def deleConnect(self , node = None):
		
		keyNode = node.hue[0].hue_FloatValue.inputs()
		if keyNode:
			self.estimateType(keyNode[0] , node)
			
		keyNode = node.colorR.inputs()
		if keyNode:
			self.estimateType(keyNode[0] , node)
		
		keyNode = node.colorB.inputs()
		if keyNode:
			self.estimateType(keyNode[0] , node)
				
		keyNode = node.colorG.inputs()
		if keyNode:
			self.estimateType(keyNode[0] , node)

	def estimateType(self , node , parnt ):
		if node.nodeType() == 'animCurveUU':
			parentNode = node.inputs()
			if not parentNode:
				pm.delete(node)
			else:
				if parentNode[0] != parnt :
					pm.delete(node)
		else:
			pm.delete(node)			



class Splitter(QtGui.QWidget):
    def __init__(self, text=None, parent=None , shadow=True, color=(150, 150, 150)):
        QtGui.QWidget.__init__(self , parent )

        self.setMinimumHeight(2)
        self.setLayout(QtGui.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignVCenter)

        first_line = QtGui.QFrame()
        first_line.setFrameStyle(QtGui.QFrame.HLine)
        self.layout().addWidget(first_line)

        main_color   = 'rgba( %s, %s, %s, 255)' %color
        shadow_color = 'rgba( 45,  45,  45, 255)'

        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' %shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:1px; \
                       %s" %(main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        first_line.setMaximumWidth(5)

        font = QtGui.QFont()
        font.setBold(True)

        text_width = QtGui.QFontMetrics(font)
        width = text_width.width(text) + 6

        label = QtGui.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.layout().addWidget(label)

        second_line = QtGui.QFrame()
        second_line.setFrameStyle(QtGui.QFrame.HLine)
        second_line.setStyleSheet(style_sheet)
        self.layout().addWidget(second_line)






AnamorphosisLinkUI()