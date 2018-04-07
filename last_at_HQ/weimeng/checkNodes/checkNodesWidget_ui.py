# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/k/k_pyside/weimeng/k_checkNodesWidget.ui'
#
# Created: Fri Jun 16 09:45:38 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_checkNodesWindow(object):
    def setupUi(self, checkNodesWindow):
        checkNodesWindow.setObjectName("checkNodesWindow")
        checkNodesWindow.resize(379, 817)
        self.centralwidget = QtGui.QWidget(checkNodesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 359, 759))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doIt_Button = QtGui.QPushButton(self.centralwidget)
        self.doIt_Button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.doIt_Button.setFont(font)
        self.doIt_Button.setObjectName("doIt_Button")
        self.horizontalLayout.addWidget(self.doIt_Button)
        self.close_Button = QtGui.QPushButton(self.centralwidget)
        self.close_Button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.close_Button.setFont(font)
        self.close_Button.setObjectName("close_Button")
        self.horizontalLayout.addWidget(self.close_Button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        checkNodesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(checkNodesWindow)
        QtCore.QMetaObject.connectSlotsByName(checkNodesWindow)

    def retranslateUi(self, checkNodesWindow):
        checkNodesWindow.setWindowTitle(QtGui.QApplication.translate("checkNodesWindow", "检查工具面板 ", None, QtGui.QApplication.UnicodeUTF8))
        self.doIt_Button.setText(QtGui.QApplication.translate("checkNodesWindow", "执行", None, QtGui.QApplication.UnicodeUTF8))
        self.close_Button.setText(QtGui.QApplication.translate("checkNodesWindow", "取消", None, QtGui.QApplication.UnicodeUTF8))

import k_checkNodesWidget_rc
