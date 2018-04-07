#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import sys
import os 
import logging 
from PySide import QtGui ,QtCore ,QtUiTools
from shiboken import wrapInstance
import maya.OpenMayaUI as OpenMayaUI 

pa = '//O:/hq_tool/Maya/hq_maya/scripts/fantabox/rigging/other/wingSys/scripts/'
#pa = '//10.99.1.12/�����Ӱ/��ʱ����/02��������/02H���ö���/0-���ù����ռ�/2016��/����/9��/9.01'
if pa not in sys.path:
	sys.path.append(pa)

import avesPlumeJoint

reload(avesPlumeJoint)


def getMayaWindow():
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr :
		return wrapInstance(long(ptr) , QtGui.QMainWindow)
		


def run():
	global Buid_win
	try:
		if Buid_win.isVisible():
			Buid_win.close()
	except:
		pass
	Buid_win = plumeUi(parent = getMayaWindow())
	Buid_win.show


class plumeUi(QtGui.QDialog):
	
	plumeCs = avesPlumeJoint.AvesPlumePitchJiont()
	
	def __init__(self , parent = None):
		super(plumeUi ,self).__init__(parent)
		
		self.verticalLayout_q = QtGui.QVBoxLayout()
		self.verticalLayout_q.setContentsMargins(5,5,5,5)
		
		self.verticalLayout_1 = QtGui.QVBoxLayout()
		self.verticalLayout_1.setContentsMargins(5,5,5,5)
		
		
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setContentsMargins(5,5,5,5)
		
		self.jointLable = QtGui.QLabel('Please Create Joint :')
		self.jointLable.setToolTip(unicode('�봴�����������','gbk'))
		self.jointLable.setWhatsThis(unicode('1 ��������������Ե�"Create Joint" ���Լ����������ٶ������ ','gbk'))
		self.jointLine = QtGui.QLineEdit()
		self.pushButton_1 = QtGui.QPushButton('Create Joint')
		self.pushButton_1.setToolTip(unicode('��������','gbk'))
		self.pushButton_5 = QtGui.QPushButton('Readin Joint')
		self.pushButton_5.setToolTip(unicode('�������','gbk'))
		
		self.verticalLayout_2.addWidget(self.jointLable)
		self.verticalLayout_2.addWidget(self.jointLine)
		self.verticalLayout_2.addWidget(self.pushButton_1)
		self.verticalLayout_2.addWidget(self.pushButton_5)
		
		self.verticalLayout_3 = QtGui.QVBoxLayout()
		self.verticalLayout_3.setContentsMargins(5,5,5,5)
		
		self.jointLable_1 = QtGui.QLabel('Create Middle Joint :')
		self.jointLable_1.setToolTip(unicode('�����м���ë����','gbk'))
		self.jointLable_1.setWhatsThis(unicode('2 �����м��������ë�м�����Ķ��� ','gbk'))
		self.horizontalLayout_1 = QtGui.QHBoxLayout()
		self.horizontalLayout_1.setContentsMargins(5,5,5,5)
		
		self.jointLable_num = QtGui.QLabel('Joint Number :')
		self.lcdNum = QtGui.QLCDNumber()
		self.slider = QtGui.QSlider()
		self.slider.setMinimum(1)
		self.slider.setMaximum(20)
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.horizontalLayout_1.addWidget(self.jointLable_num)
		self.horizontalLayout_1.addWidget(self.lcdNum)
		self.horizontalLayout_1.addWidget(self.slider)
		
		self.verticalLayout_3.addWidget(self.jointLable_1)
		self.verticalLayout_3.addLayout(self.horizontalLayout_1)
		
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setContentsMargins(5,0,5,5)
		
		self.pushButton_2 = QtGui.QPushButton('Create Bird Plumage')
		self.pushButton_2.setToolTip(unicode('����������ë','gbk'))
		
		self.verticalLayout_4.addWidget(self.pushButton_2 )
		
		self.verticalLayout_5 = QtGui.QVBoxLayout()
		self.verticalLayout_5.setContentsMargins(5,0,5,5)
		
		self.jointLable_2 = QtGui.QLabel('Multilayer Joint :')
		self.jointLable_2.setToolTip(unicode('����������','gbk'))
		self.jointLable_2.setWhatsThis(unicode('3 ������������','gbk'))
		self.pushButton_3 = QtGui.QPushButton('Add Joint')
		self.pushButton_3.setToolTip(unicode('��ӹ���','gbk'))
		self.pushButton_4 = QtGui.QPushButton('Create')
		self.pushButton_4.setToolTip(unicode('����','gbk'))
		
		self.verticalLayout_5.addWidget(self.jointLable_2 )
		self.verticalLayout_5.addWidget(self.pushButton_3 )
		self.verticalLayout_5.addWidget(self.pushButton_4 )
		
		
		self.verticalLayout_1.addLayout(self.verticalLayout_2)
		self.verticalLayout_1.addLayout(self.verticalLayout_3)
		self.verticalLayout_1.addLayout(self.verticalLayout_4)
		self.verticalLayout_1.addLayout(self.verticalLayout_5)
		
		
		
		self.groupBox = QtGui.QGroupBox()
		
		self.groupBox.setMinimumSize(QtCore.QSize(300, 325))
		self.groupBox.setMaximumSize(QtCore.QSize(300, 325))
		
		self.groupBox.setLayout(self.verticalLayout_1)
		
		self.verticalLayout_q.addWidget(self.groupBox)

		
		self.setLayout(self.verticalLayout_q)
		
		self.makeConnections()
		self.setWindowTitle("BIRD PLUMAGE UI")
		
		self.resize(310, 335)
		self.setMinimumSize(QtCore.QSize(310, 335))
		self.setObjectName('BIRD UI')
		self.initUiState()
		self.show()
		
	def makeConnections(self):
		self.pushButton_1.clicked.connect(self.createJoint)
		self.pushButton_2.clicked.connect(self.biud)
		self.pushButton_3.clicked.connect(self.addCreateJoint)
		self.pushButton_4.clicked.connect(self.addBiud)
		self.pushButton_5.clicked.connect(self.readin)

		self.slider.valueChanged.connect(self.lcdNum.display)
		
	def initUiState(self):
		
		self.jointLine.setEnabled(False)
		self.jointLine.setPlaceholderText('Joint Name')
		self.slider.setValue(6)
		self.lcdNum.display(6)
		
	def createJoint(self):
		plumeUi.plumeCs._biudPitchJoint()
		name = [a.name() for a in plumeUi.plumeCs.leftList]
		txt = ' , '.join(name)
		self.jointLine.setText('name: %s'%(txt))
	
	
	def biud(self):
		num_n = self.slider.value()
		txt1 = self.jointLine.text()
		if txt1 == 'Joint Name' or not txt1:
			logger.error('not obj')
			return 
		
		plumeUi.plumeCs.biud(num_n)
	
	
	def addCreateJoint(self):
		plumeUi.plumeCs._addBiudPitchJoint()
		
	
	def addBiud(self):
		plumeUi.plumeCs.addBuid()
		
	def readin(self):
		plumeUi.plumeCs.readinJoint()
		name = [a.name() for a in plumeUi.plumeCs.leftList]
		txt = ' , '.join(name)
		self.jointLine.setText('name: %s'%(txt))
		
		
		

#def PlumeUI():
if __name__=='__main__':

    run()




