# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/k/k_pyside/weimeng/checkNodeForMayaReplyWin.ui'
#
# Created: Thu Jun 15 12:01:38 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(391, 672)
        self.k_centralwidget = QtGui.QWidget(MainWindow)
        self.k_centralwidget.setObjectName("k_centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.k_centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtGui.QToolBox(self.k_centralwidget)
        self.toolBox.setObjectName("toolBox")
        self.k_page = QtGui.QWidget()
        self.k_page.setGeometry(QtCore.QRect(0, 0, 373, 628))
        self.k_page.setObjectName("k_page")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.k_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox.addItem(self.k_page, "")
        self.verticalLayout.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.k_centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.k_page), QtGui.QApplication.translate("MainWindow", "无发现不符合规定节点", None, QtGui.QApplication.UnicodeUTF8))

