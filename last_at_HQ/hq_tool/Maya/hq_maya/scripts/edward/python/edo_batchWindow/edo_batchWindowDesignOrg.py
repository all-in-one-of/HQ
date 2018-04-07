# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/program/edward/python/edo_batchWindow/edo_batchWindowDesigna.ui'
#
# Created: Wed Nov 06 11:13:04 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_edo_batchWindow(object):
    def setupUi(self, edo_batchWindow):
        edo_batchWindow.setObjectName(_fromUtf8("edo_batchWindow"))
        edo_batchWindow.resize(379, 529)
        edo_batchWindow.setWindowTitle(QtGui.QApplication.translate("edo_batchWindow", "edo_batchWindow", None, QtGui.QApplication.UnicodeUTF8))
        edo_batchWindow.setWindowOpacity(0.95)
        edo_batchWindow.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(100, 80, 80, 255), stop:1 rgba(230, 230, 180, 255))"))
        self.centralwidget = QtGui.QWidget(edo_batchWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.batchBt = QtGui.QPushButton(self.centralwidget)
        self.batchBt.setGeometry(QtCore.QRect(30, 430, 319, 57))
        self.batchBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground001.jpg);\n"
"font: 75 12pt \"幼圆\";"))
        self.batchBt.setText(QtGui.QApplication.translate("edo_batchWindow", "BATCH", None, QtGui.QApplication.UnicodeUTF8))
        self.batchBt.setObjectName(_fromUtf8("batchBt"))
        self.saveToThisPath = QtGui.QRadioButton(self.centralwidget)
        self.saveToThisPath.setGeometry(QtCore.QRect(10, 340, 141, 31))
        self.saveToThisPath.setStyleSheet(_fromUtf8("background:rgba(0,0,0,0);"))
        self.saveToThisPath.setText(QtGui.QApplication.translate("edo_batchWindow", "save to the path below", None, QtGui.QApplication.UnicodeUTF8))
        self.saveToThisPath.setObjectName(_fromUtf8("saveToThisPath"))
        self.savePath = QtGui.QLineEdit(self.centralwidget)
        self.savePath.setEnabled(True)
        self.savePath.setGeometry(QtCore.QRect(10, 380, 361, 31))
        self.savePath.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(80, 80, 80, 255), stop:1 rgba(120, 120, 120, 200))"))
        self.savePath.setText(_fromUtf8(""))
        self.savePath.setObjectName(_fromUtf8("savePath"))
        self.script1 = QtGui.QLineEdit(self.centralwidget)
        self.script1.setGeometry(QtCore.QRect(60, 300, 311, 31))
        self.script1.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(180, 180, 180, 255), stop:1 rgba(250, 250, 250, 200))"))
        self.script1.setText(_fromUtf8(""))
        self.script1.setObjectName(_fromUtf8("script1"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 310, 46, 13))
        self.label.setStyleSheet(_fromUtf8("background:rgba(0,0,0,0);"))
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setLineWidth(1)
        self.label.setText(QtGui.QApplication.translate("edo_batchWindow", "script:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.listText = QtGui.QLabel(self.centralwidget)
        self.listText.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.listText.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(180, 180, 180, 255), stop:1 rgba(250, 250, 250, 200))"))
        self.listText.setFrameShape(QtGui.QFrame.Box)
        self.listText.setLineWidth(2)
        self.listText.setText(_fromUtf8(""))
        self.listText.setObjectName(_fromUtf8("listText"))
        self.exe = QtGui.QLineEdit(self.centralwidget)
        self.exe.setGeometry(QtCore.QRect(60, 260, 311, 31))
        self.exe.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(180, 180, 180, 255), stop:1 rgba(250, 250, 250, 200))"))
        self.exe.setText(_fromUtf8(""))
        self.exe.setObjectName(_fromUtf8("exe"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 270, 46, 13))
        self.label_2.setStyleSheet(_fromUtf8("background:rgba(0,0,0,0);"))
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setLineWidth(1)
        self.label_2.setText(QtGui.QApplication.translate("edo_batchWindow", "exe:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        edo_batchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(edo_batchWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 379, 18))
        self.menubar.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(120, 120, 150, 255), stop:1 rgba(180, 180, 200, 200))"))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        edo_batchWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(edo_batchWindow)
        self.statusbar.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(180, 180, 180, 200), stop:1 rgba(250, 250, 250, 200))"))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        edo_batchWindow.setStatusBar(self.statusbar)

        self.retranslateUi(edo_batchWindow)
        QtCore.QMetaObject.connectSlotsByName(edo_batchWindow)

    def retranslateUi(self, edo_batchWindow):
        pass

import edo_batchWindow_rc
