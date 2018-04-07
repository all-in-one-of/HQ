# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/program/edward/python/edo_skinWeightIoUI/edo_skinWeightIoUI.ui'
#
# Created: Wed Apr 23 17:27:39 2014
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_edo_skinWeightIoUI(object):
    def setupUi(self, edo_skinWeightIoUI):
        edo_skinWeightIoUI.setObjectName(_fromUtf8("edo_skinWeightIoUI"))
        edo_skinWeightIoUI.resize(438, 452)
        edo_skinWeightIoUI.setWindowTitle(QtGui.QApplication.translate("edo_skinWeightIoUI", "edo_skinWeightIoUI", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(edo_skinWeightIoUI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.edo_skinWeightIoLayout = QtGui.QTabWidget(self.centralwidget)
        self.edo_skinWeightIoLayout.setGeometry(QtCore.QRect(0, 10, 431, 401))
        self.edo_skinWeightIoLayout.setObjectName(_fromUtf8("edo_skinWeightIoLayout"))
        self.IO_skinweight = QtGui.QWidget()
        self.IO_skinweight.setObjectName(_fromUtf8("IO_skinweight"))
        self.ex_bt = QtGui.QPushButton(self.IO_skinweight)
        self.ex_bt.setGeometry(QtCore.QRect(10, 10, 411, 51))
        self.ex_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "export skinWeight", None, QtGui.QApplication.UnicodeUTF8))
        self.ex_bt.setObjectName(_fromUtf8("ex_bt"))
        self.md_bt = QtGui.QPushButton(self.IO_skinweight)
        self.md_bt.setGeometry(QtCore.QRect(320, 80, 101, 71))
        self.md_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "modify skinWeight", None, QtGui.QApplication.UnicodeUTF8))
        self.md_bt.setObjectName(_fromUtf8("md_bt"))
        self.im_bt = QtGui.QPushButton(self.IO_skinweight)
        self.im_bt.setGeometry(QtCore.QRect(10, 170, 411, 51))
        self.im_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "import skinWeight", None, QtGui.QApplication.UnicodeUTF8))
        self.im_bt.setObjectName(_fromUtf8("im_bt"))
        self.sw_line = QtGui.QLineEdit(self.IO_skinweight)
        self.sw_line.setGeometry(QtCore.QRect(90, 79, 221, 31))
        self.sw_line.setObjectName(_fromUtf8("sw_line"))
        self.rp_line = QtGui.QLineEdit(self.IO_skinweight)
        self.rp_line.setGeometry(QtCore.QRect(90, 120, 221, 31))
        self.rp_line.setObjectName(_fromUtf8("rp_line"))
        self.label = QtGui.QLabel(self.IO_skinweight)
        self.label.setGeometry(QtCore.QRect(20, 90, 71, 16))
        self.label.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "SKIN WEIGHT", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.IO_skinweight)
        self.label_2.setGeometry(QtCore.QRect(20, 130, 71, 16))
        self.label_2.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "REPLACE", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.edo_skinWeightIoLayout.addTab(self.IO_skinweight, _fromUtf8(""))
        self.Edit_skinweight = QtGui.QWidget()
        self.Edit_skinweight.setObjectName(_fromUtf8("Edit_skinweight"))
        self.saveTemp_bt = QtGui.QPushButton(self.Edit_skinweight)
        self.saveTemp_bt.setGeometry(QtCore.QRect(10, 330, 411, 41))
        self.saveTemp_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "FINISH", None, QtGui.QApplication.UnicodeUTF8))
        self.saveTemp_bt.setObjectName(_fromUtf8("saveTemp_bt"))
        self.sourseInfluence = QtGui.QListWidget(self.Edit_skinweight)
        self.sourseInfluence.setGeometry(QtCore.QRect(10, 30, 201, 181))
        self.sourseInfluence.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.sourseInfluence.setObjectName(_fromUtf8("sourseInfluence"))
        self.directInfluence = QtGui.QListWidget(self.Edit_skinweight)
        self.directInfluence.setGeometry(QtCore.QRect(220, 30, 201, 181))
        self.directInfluence.setObjectName(_fromUtf8("directInfluence"))
        self.direct_bt = QtGui.QPushButton(self.Edit_skinweight)
        self.direct_bt.setGeometry(QtCore.QRect(220, 220, 201, 41))
        self.direct_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "LOAD", None, QtGui.QApplication.UnicodeUTF8))
        self.direct_bt.setObjectName(_fromUtf8("direct_bt"))
        self.source_bt = QtGui.QPushButton(self.Edit_skinweight)
        self.source_bt.setGeometry(QtCore.QRect(10, 220, 201, 41))
        self.source_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "LOAD", None, QtGui.QApplication.UnicodeUTF8))
        self.source_bt.setObjectName(_fromUtf8("source_bt"))
        self.addTemp_bt = QtGui.QPushButton(self.Edit_skinweight)
        self.addTemp_bt.setGeometry(QtCore.QRect(10, 280, 411, 41))
        self.addTemp_bt.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "ADD TO TEMPLATE", None, QtGui.QApplication.UnicodeUTF8))
        self.addTemp_bt.setObjectName(_fromUtf8("addTemp_bt"))
        self.edo_skinWeightIoLayout.addTab(self.Edit_skinweight, _fromUtf8(""))
        edo_skinWeightIoUI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(edo_skinWeightIoUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("edo_skinWeightIoUI", "help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        edo_skinWeightIoUI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(edo_skinWeightIoUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        edo_skinWeightIoUI.setStatusBar(self.statusbar)
        self.actionHow_to_use = QtGui.QAction(edo_skinWeightIoUI)
        self.actionHow_to_use.setText(QtGui.QApplication.translate("edo_skinWeightIoUI", "how_to_use", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHow_to_use.setObjectName(_fromUtf8("actionHow_to_use"))
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(edo_skinWeightIoUI)
        self.edo_skinWeightIoLayout.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(edo_skinWeightIoUI)

    def retranslateUi(self, edo_skinWeightIoUI):
        self.edo_skinWeightIoLayout.setTabText(self.edo_skinWeightIoLayout.indexOf(self.IO_skinweight), QtGui.QApplication.translate("edo_skinWeightIoUI", "IO_skinweight", None, QtGui.QApplication.UnicodeUTF8))
        self.edo_skinWeightIoLayout.setTabText(self.edo_skinWeightIoLayout.indexOf(self.Edit_skinweight), QtGui.QApplication.translate("edo_skinWeightIoUI", "Edit_skinweight", None, QtGui.QApplication.UnicodeUTF8))

