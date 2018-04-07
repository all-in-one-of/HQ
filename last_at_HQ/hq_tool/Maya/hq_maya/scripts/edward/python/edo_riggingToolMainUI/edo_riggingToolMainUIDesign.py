# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/program/edward/python/edo_riggingToolMainUI/edo_riggingToolMainUIDesign.ui'
#
# Created: Fri Jun 20 13:01:21 2014
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_edo_riggingToolMainUI(object):
    def setupUi(self, edo_riggingToolMainUI):
        edo_riggingToolMainUI.setObjectName(_fromUtf8("edo_riggingToolMainUI"))
        edo_riggingToolMainUI.resize(329, 566)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(edo_riggingToolMainUI.sizePolicy().hasHeightForWidth())
        edo_riggingToolMainUI.setSizePolicy(sizePolicy)
        edo_riggingToolMainUI.setWindowTitle(QtGui.QApplication.translate("edo_riggingToolMainUI", "edo_riggingToolMainUI", None, QtGui.QApplication.UnicodeUTF8))
        edo_riggingToolMainUI.setWindowOpacity(0.9)
        edo_riggingToolMainUI.setAutoFillBackground(False)
        edo_riggingToolMainUI.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/windowBackground002.jpg)"))
        edo_riggingToolMainUI.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(edo_riggingToolMainUI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 311, 531))
        self.tabWidget.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(80, 80, 90, 100), stop:1 rgba(180, 180, 220, 5))"))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.rig_tab = QtGui.QWidget()
        self.rig_tab.setObjectName(_fromUtf8("rig_tab"))
        self.IkFkChainCtrlTool_Bt = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt.setGeometry(QtCore.QRect(10, 10, 87, 86))
        self.IkFkChainCtrlTool_Bt.setStyleSheet(_fromUtf8("font: italic 10pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground001.jpg);\n"
"\n"
""))
        self.IkFkChainCtrlTool_Bt.setText(QtGui.QApplication.translate("edo_riggingToolMainUI", "IKFK\n"
"Chain", None, QtGui.QApplication.UnicodeUTF8))
        self.IkFkChainCtrlTool_Bt.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt"))
        self.IkFkChainCtrlTool_Bt_17 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_17.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_17.setGeometry(QtCore.QRect(10, 110, 87, 86))
        self.IkFkChainCtrlTool_Bt_17.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_17.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_17.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_17"))
        self.IkFkChainCtrlTool_Bt_27 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_27.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_27.setGeometry(QtCore.QRect(110, 410, 87, 86))
        self.IkFkChainCtrlTool_Bt_27.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_27.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_27.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_27"))
        self.IkFkChainCtrlTool_Bt_24 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_24.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_24.setGeometry(QtCore.QRect(110, 310, 87, 86))
        self.IkFkChainCtrlTool_Bt_24.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_24.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_24.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_24"))
        self.blendshapeTool_Bt = QtGui.QPushButton(self.rig_tab)
        self.blendshapeTool_Bt.setGeometry(QtCore.QRect(110, 10, 87, 86))
        self.blendshapeTool_Bt.setStyleSheet(_fromUtf8("font: italic 10pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground001.jpg);\n"
"\n"
""))
        self.blendshapeTool_Bt.setText(QtGui.QApplication.translate("edo_riggingToolMainUI", "BLEND\n"
"SHAPE", None, QtGui.QApplication.UnicodeUTF8))
        self.blendshapeTool_Bt.setObjectName(_fromUtf8("blendshapeTool_Bt"))
        self.IkFkChainCtrlTool_Bt_22 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_22.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_22.setGeometry(QtCore.QRect(10, 210, 87, 86))
        self.IkFkChainCtrlTool_Bt_22.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_22.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_22.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_22"))
        self.IkFkChainCtrlTool_Bt_21 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_21.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_21.setGeometry(QtCore.QRect(110, 210, 87, 86))
        self.IkFkChainCtrlTool_Bt_21.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_21.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_21.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_21"))
        self.IkFkChainCtrlTool_Bt_23 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_23.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_23.setGeometry(QtCore.QRect(210, 310, 87, 86))
        self.IkFkChainCtrlTool_Bt_23.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_23.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_23.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_23"))
        self.IkFkChainCtrlTool_Bt_28 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_28.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_28.setGeometry(QtCore.QRect(10, 410, 87, 86))
        self.IkFkChainCtrlTool_Bt_28.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_28.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_28.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_28"))
        self.IkFkChainCtrlTool_Bt_3 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_3.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_3.setGeometry(QtCore.QRect(210, 10, 87, 86))
        self.IkFkChainCtrlTool_Bt_3.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_3.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_3.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_3"))
        self.IkFkChainCtrlTool_Bt_18 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_18.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_18.setGeometry(QtCore.QRect(110, 110, 87, 86))
        self.IkFkChainCtrlTool_Bt_18.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_18.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_18.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_18"))
        self.IkFkChainCtrlTool_Bt_20 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_20.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_20.setGeometry(QtCore.QRect(210, 210, 87, 86))
        self.IkFkChainCtrlTool_Bt_20.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_20.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_20.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_20"))
        self.IkFkChainCtrlTool_Bt_25 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_25.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_25.setGeometry(QtCore.QRect(10, 310, 87, 86))
        self.IkFkChainCtrlTool_Bt_25.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_25.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_25.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_25"))
        self.IkFkChainCtrlTool_Bt_19 = QtGui.QPushButton(self.rig_tab)
        self.IkFkChainCtrlTool_Bt_19.setEnabled(False)
        self.IkFkChainCtrlTool_Bt_19.setGeometry(QtCore.QRect(210, 110, 87, 86))
        self.IkFkChainCtrlTool_Bt_19.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.IkFkChainCtrlTool_Bt_19.setText(_fromUtf8(""))
        self.IkFkChainCtrlTool_Bt_19.setObjectName(_fromUtf8("IkFkChainCtrlTool_Bt_19"))
        self.BodyRigTool_Bt = QtGui.QPushButton(self.rig_tab)
        self.BodyRigTool_Bt.setEnabled(False)
        self.BodyRigTool_Bt.setGeometry(QtCore.QRect(210, 410, 87, 86))
        self.BodyRigTool_Bt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/buttonBackground002.jpg);\n"
""))
        self.BodyRigTool_Bt.setText(_fromUtf8(""))
        self.BodyRigTool_Bt.setObjectName(_fromUtf8("BodyRigTool_Bt"))
        self.tabWidget.addTab(self.rig_tab, _fromUtf8(""))
        self.simulation_tab = QtGui.QWidget()
        self.simulation_tab.setObjectName(_fromUtf8("simulation_tab"))
        self.tabWidget.addTab(self.simulation_tab, _fromUtf8(""))
        self.animation_tab = QtGui.QWidget()
        self.animation_tab.setObjectName(_fromUtf8("animation_tab"))
        self.riggingCtrlPanel_Bt = QtGui.QPushButton(self.animation_tab)
        self.riggingCtrlPanel_Bt.setGeometry(QtCore.QRect(10, 10, 87, 86))
        self.riggingCtrlPanel_Bt.setStyleSheet(_fromUtf8("font: italic 10pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground001.jpg);\n"
"\n"
""))
        self.riggingCtrlPanel_Bt.setText(QtGui.QApplication.translate("edo_riggingToolMainUI", "Rigging\n"
"Ctrl Panel", None, QtGui.QApplication.UnicodeUTF8))
        self.riggingCtrlPanel_Bt.setObjectName(_fromUtf8("riggingCtrlPanel_Bt"))
        self.riggingFileControler_Bt = QtGui.QPushButton(self.animation_tab)
        self.riggingFileControler_Bt.setGeometry(QtCore.QRect(110, 10, 87, 86))
        self.riggingFileControler_Bt.setStyleSheet(_fromUtf8("font: italic 10pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground001.jpg);\n"
"\n"
""))
        self.riggingFileControler_Bt.setText(QtGui.QApplication.translate("edo_riggingToolMainUI", "Rigging\n"
"File\n"
"Controler", None, QtGui.QApplication.UnicodeUTF8))
        self.riggingFileControler_Bt.setObjectName(_fromUtf8("riggingFileControler_Bt"))
        self.tabWidget.addTab(self.animation_tab, _fromUtf8(""))
        edo_riggingToolMainUI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(edo_riggingToolMainUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 329, 18))
        self.menubar.setStyleSheet(_fromUtf8("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(120,120, 120, 255), stop:1 rgba(200, 200, 200, 255))"))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("edo_riggingToolMainUI", "help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        edo_riggingToolMainUI.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(edo_riggingToolMainUI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(edo_riggingToolMainUI)

    def retranslateUi(self, edo_riggingToolMainUI):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rig_tab), QtGui.QApplication.translate("edo_riggingToolMainUI", "RIGGING", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.simulation_tab), QtGui.QApplication.translate("edo_riggingToolMainUI", "SIMULATION", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.animation_tab), QtGui.QApplication.translate("edo_riggingToolMainUI", "ANIMATION", None, QtGui.QApplication.UnicodeUTF8))

import edo_buildControlerFromSkeletonUI_rc
