import pymel.core as pm 
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance
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

		self.label2 = QtGui.QLabel('SG Node Name')
		self.qGrid1.addWidget(self.label2 , 1 , 0 )
		
		self.linetxt2 = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxt2 , 1 , 1)
		
		self.PushButton2 = QtGui.QPushButton('Get')
		self.qGrid1.addWidget(self.PushButton2, 1 , 2)
		
		self.linetxt3 = QtGui.QLineEdit()
		self.qGrid1.addWidget(self.linetxt3 , 1 , 3)
		
		self.qGrid2 = QtGui.QGridLayout()
		self.qGrid1.setContentsMargins(5,5,5,5)
		self.QVBoxLayout.addLayout(self.qGrid2)
		
		self.colotButtonList = [self.colotButton(i , self.qGrid2) for i in range(9)]
		
		self.okButton = QtGui.QPushButton('Set Driven Keyframe')
		self.QVBoxLayout.addWidget(self.okButton)
		
		self.makeConnections()
		self.setWindowTitle("SG Node UI")
		
		self.resize(450, 153)
		self.setMinimumSize(QtCore.QSize(450, 153))
		self.setMaximumSize(QtCore.QSize(450, 153))
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
		self.okButton.clicked.connect(self.sg_connectAttr)
		self.comBox.activated.connect(self.setBox1)
		
		for ide,bn in enumerate(self.colotButtonList):
			bn.clicked.connect(functools.partial(self.setColor1 , ide))
			bn.clicked.connect(bn.setDown)
	
	def initUiState(self):
		self.linetxt1.setText(str(self.ctrName))
		self.linetxt1.setEnabled(False)
		self.linetxt2.setText(str(self.nodeName))
		self.linetxt2.setEnabled(False)
		self.linetxt3.setEnabled(False)
		self.getCtrLAttrList()
		
	
	def setColor1(self ,color1 = None):
		node = pm.PyNode(self.nodeName)
		if node.hasAttr('color'):
			self.linetxt3.setText(str(self.colorMapDict.get(color1)[1]))
			node.hue[0].hue_FloatValue.set(self.colorMapDict.get(color1)[1])
			node.color.set(self.colorMapDict.get(color1)[0])

	def setBox1(self):
		txt = self.comBox.currentText()
		main = pm.PyNode(self.ctrName)
		main.tex.set(int(txt))
					
	
	def setTxt1(self):
		self.ctrName = self.sg_selectName() 
		self.linetxt1.setText(str(self.ctrName))
		if self.linetxt1.text() != 'None':
			self.getCtrLAttrList()
			
	
	def setTxt2(self):
		self.nodeName = self.sg_selectName()
		if pm.PyNode(self.nodeName).type() == 'remapHsv':
			self.linetxt2.setText(str(self.nodeName))
			OpenMaya.MGlobal_displayInfo('<<<<<<<< Load Ok >>>>>>>>')
		else:
			OpenMaya.MGlobal_displayWarning('Select object not is remapHsv node ,%s is %s type'%(self.nodeName , pm.PyNode(self.nodeName).type()))
			return
	
	def sg_connectAttr(self):
		mian = pm.PyNode(self.ctrName)
		rbg = pm.PyNode(self.nodeName)
		rbg.hue[0].hue_FloatValue.set(float(self.linetxt3.text()))
		if mian.hasAttr('tex'):
			
			pm.setDrivenKeyframe(rbg.hue[0].hue_FloatValue , currentDriver = mian.tex , itt = 'linear' , ott = 'linear')
			pm.setDrivenKeyframe(rbg.color , currentDriver = mian.tex , itt = 'linear' , ott = 'linear')
		
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
			if main.hasAttr('tex'):
				emDirt = main.tex.getEnums()
				enDirtKey = emDirt.keys()
				self.comBox.clear()
				self.comBox.addItems(enDirtKey)
				OpenMaya.MGlobal_displayInfo('<<<<<<<< Load Ok >>>>>>>>')
			else :
				self.comBox.clear()
				OpenMaya.MGlobal_displayWarning('Select ctrl not is tex attribute , Again select .....')
				
				
class TexChangeTool(object):
	def __init__(self):
		self.main =  None
		self.rgbNode = None	
		self.win = None			
	
	def texlink(self):
		if pm.objExists('Main'):
			self.main = pm.PyNode('Main') 
		else:
			OpenMaya.MGlobal_displayError('not Main ctrl')
			return
		
		if 'alSwitchColor' in pm.allNodeTypes():
			all = pm.ls(type = 'alSwitchColor')
			if all:
				pat = [a for a in all if a.outputs(type= 'alSwitchColor')][0]
				file1 = pat.inputs(type = 'file')
				num =[str(i) for i in range(len(file1))]
				enstr = ':'.join(num)
				if not self.main.hasAttr('tex'):
					self.main.addAttr('tex' , at = 'enum' , en = enstr , k = True)
				if self.main.tex not in pat.mix.inputs(p = True):
					self.main.tex.connect(pat.mix , f = True)
				out = pat.outputs()[0]
				self.getSG(out)
				
				if self.SGNode:
					nodeList = self.SGNode.inputs()[0].inputs()
					
					for n in nodeList:
						if n.type() == 'remapHsv':
							self.rgbNode = n
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
				
				
				
										
	def getSG(self , node = None):
		if node.type() == 'shadingEngine':
			self.SGNode = node
		else :
			outList = node.outputs()
			if outList:
				for out in outList:
					self.getSG(out)			





tex = TexChangeTool()
tex.texlink()
