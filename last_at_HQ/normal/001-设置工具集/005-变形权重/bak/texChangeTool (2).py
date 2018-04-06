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
							8:[(200,0,200) , 0.85]}
		
		self.ctrName = ctrName 
		self.nodeName = nodeName
		self.geoName = None
		
		
		self.QVBoxLayout = QtGui.QVBoxLayout()
		self.QVBoxLayout.setContentsMargins(5,5,5,5)
		
		self.qGroupBox = QtGui.QGroupBox('Get Control And SG Node Name')
		self.QVBoxLayout.addWidget(self.qGroupBox)
		
		self.qGrid1 = QtGui.QGridLayout()
		self.qGrid1.setContentsMargins(5,5,5,5)
		self.qGroupBox.setLayout(self.qGrid1)
		
		self.label1 = QtGui.QLabel('Control Name')
		self.qGrid1.addWidget(self.label1 , 0 , 0)
		
		self.linetxt1 = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxt1 , 0 , 1 )
		
		self.PushButton1 = QtGui.QPushButton('Get')
		self.qGrid1.addWidget(self.PushButton1 , 0 , 2 )
		
		self.comBox = QtGui.QComboBox()
		self.qGrid1.addWidget(self.comBox , 0 , 3  )
		
		self.labelm = QtGui.QLabel('Tou Geo Name')
		self.qGrid1.addWidget(self.labelm , 1 , 0)
		
		self.linetxtm = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxtm , 1 , 1)
		
		self.PushButtonm = QtGui.QPushButton('Get')
		self.qGrid1.addWidget(self.PushButtonm, 1 , 2)

		self.label2 = QtGui.QLabel('SG Node Name')
		self.qGrid1.addWidget(self.label2 , 2 , 0 )
		
		self.linetxt2 = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxt2 , 2 , 1)
		
		self.PushButton2 = QtGui.QPushButton('Get')
		self.qGrid1.addWidget(self.PushButton2, 2 , 2)
		
		self.linetxt3 = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxt3 , 2 , 3)
		
		self.qGrid2 = QtGui.QGridLayout()
		self.qGrid1.setContentsMargins(5,5,5,5)
		self.QVBoxLayout.addLayout(self.qGrid2)
		
		self.colotButtonList = [self.colotButton(i , self.qGrid2) for i in range(9)]
		
		self.okButton = QtGui.QPushButton('Set Driven Keyframe')
		self.QVBoxLayout.addWidget(self.okButton)
		
		self.makeConnections()
		self.setWindowTitle("SG Node UI")
		
		self.resize(450, 183)
		self.setMinimumSize(QtCore.QSize(450, 183))
		self.setMaximumSize(QtCore.QSize(450, 183))
		self.setLayout(self.QVBoxLayout)
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
		self.getCtrLAttrList()
		
	
	def setColor1(self ,color1 = None):
		node = pm.PyNode(self.nodeName)
		if node.hasAttr('color'):
			self.linetxt3.setText(str(self.colorMapDict.get(color1)[1]))
			node.hue[0].hue_FloatValue.set(self.colorMapDict.get(color1)[1])
			node.color.set(self.colorMapDict.get(color1)[0])

	def setBox1(self):
		txt = self.comBox.currentIndex()
		main = pm.PyNode(self.ctrName)
		main.fileTextureName.set(int(txt))
					
	
	def setTxt1(self):
		ctrName = self.sg_selectName()
		if not ctrName:
			OpenMaya.MGlobal_displayError('not select object ctrl, please again select')
			return 
		self.ctrName = ctrName
		self.linetxt1.setText(str(self.ctrName))
		if self.linetxt1.text() != 'None':
			self.getCtrLAttrList()
			
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

		if not geo.hasAttr('fileTextureName'):
			emDirt = main.fileTextureName.getEnums()
			enDirtKey = emDirt.keys()
			enstr = ':'.join(enDirtKey)
			geo.addAttr('fileTextureName' , at = 'enum' , en = enstr , k = True)
			
		if main.fileTextureName not in geo.fileTextureName.inputs(p = True):
			main.fileTextureName.connect(geo.fileTextureName , f = True)
			
		if geo.fileTextureName not in rbg.fileTextureName.inputs(p = True):
			geo.fileTextureName.connect(rbg.fileTextureName , f = True)
		
	def sg_selectName(self):
		sel = pm.ls(sl=True)
		if sel:
			s = sel[0].name()
			return s
		else:
			return None
			
	def getCtrLAttrList(self):
		if self.ctrName :
			main = pm.PyNode(self.ctrName)
			if main.hasAttr('fileTextureName'):
				emDirt = main.fileTextureName.getEnums()
				enDirtKey = emDirt.keys()
				self.comBox.clear()
				self.comBox.addItems(enDirtKey)
				OpenMaya.MGlobal_displayInfo('<<<<<<<< Load Ok >>>>>>>>')
			else :
				self.comBox.clear()
				
				OpenMaya.MGlobal_displayWarning('Select ctrl not is fileTextureName attribute , Again select .....')
				
				
class TexChangeTool(object):
	def __init__(self):
		self.main =  None
		self.rgbNode = None	
		self.win = None	
		self.attrList = list('abcdefghijk')
	
	
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
				file1 = pat.input.inputs()
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
				
				if self.rgbNode.fileTextureName not in pat.selector.inputs(p = True):
					self.rgbNode.fileTextureName.connect(pat.selector , f = True)
					
				if not self.rgbNode.fileTextureName.inputs():
					self.main.fileTextureName.connect(self.rgbNode.fileTextureName ,f = True)
				
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
		    
		    
		self.win = AnamorphosisLinkUI(ctrName , rgbName)
		
				
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
						return hav
				
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



tex = TexChangeTool()
tex.texlink()