# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '//10.99.1.12/�����Ӱ/��ʱ����/08����/�����ļ���/H��˧/adv5/AdvancedSkeleton5/AdvancedSkeleton5Files/icons/advanceSkeleton5.0.ui'
#
# Created: Tue Jan 12 19:27:19 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_advancedSkeletonWin(object):
    def setupUi(self, advancedSkeletonWin):
        advancedSkeletonWin.setObjectName("advancedSkeletonWin")
        advancedSkeletonWin.resize(512, 443)
        advancedSkeletonWin.setMinimumSize(QtCore.QSize(512, 443))
        self.centralwidget = QtGui.QWidget(advancedSkeletonWin)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 491, 181))
        self.groupBox.setStyleSheet("font: italic 14pt \"Brush Script MT\";")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.AS5_Button = QtGui.QPushButton(self.groupBox)
        self.AS5_Button.setGeometry(QtCore.QRect(10, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AS5_Button.sizePolicy().hasHeightForWidth())
        self.AS5_Button.setSizePolicy(sizePolicy)
        self.AS5_Button.setStyleSheet("")
        self.AS5_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/ADVRig.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AS5_Button.setIcon(icon)
        self.AS5_Button.setIconSize(QtCore.QSize(151, 71))
        self.AS5_Button.setObjectName("AS5_Button")
        self.bodySelector_Button = QtGui.QPushButton(self.groupBox)
        self.bodySelector_Button.setGeometry(QtCore.QRect(170, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bodySelector_Button.sizePolicy().hasHeightForWidth())
        self.bodySelector_Button.setSizePolicy(sizePolicy)
        self.bodySelector_Button.setStyleSheet("")
        self.bodySelector_Button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/bodySeletor.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bodySelector_Button.setIcon(icon1)
        self.bodySelector_Button.setIconSize(QtCore.QSize(151, 71))
        self.bodySelector_Button.setObjectName("bodySelector_Button")
        self.facialSelector_Button = QtGui.QPushButton(self.groupBox)
        self.facialSelector_Button.setGeometry(QtCore.QRect(330, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.facialSelector_Button.sizePolicy().hasHeightForWidth())
        self.facialSelector_Button.setSizePolicy(sizePolicy)
        self.facialSelector_Button.setStyleSheet("")
        self.facialSelector_Button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/faceSelector.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.facialSelector_Button.setIcon(icon2)
        self.facialSelector_Button.setIconSize(QtCore.QSize(151, 71))
        self.facialSelector_Button.setObjectName("facialSelector_Button")
        self.bodyOptimize_Button = QtGui.QPushButton(self.groupBox)
        self.bodyOptimize_Button.setGeometry(QtCore.QRect(10, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bodyOptimize_Button.sizePolicy().hasHeightForWidth())
        self.bodyOptimize_Button.setSizePolicy(sizePolicy)
        self.bodyOptimize_Button.setStyleSheet("")
        self.bodyOptimize_Button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/bodyOptimize.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bodyOptimize_Button.setIcon(icon3)
        self.bodyOptimize_Button.setIconSize(QtCore.QSize(151, 71))
        self.bodyOptimize_Button.setObjectName("bodyOptimize_Button")
        self.faceOptimize_Button = QtGui.QPushButton(self.groupBox)
        self.faceOptimize_Button.setEnabled(True)
        self.faceOptimize_Button.setGeometry(QtCore.QRect(170, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.faceOptimize_Button.sizePolicy().hasHeightForWidth())
        self.faceOptimize_Button.setSizePolicy(sizePolicy)
        self.faceOptimize_Button.setStyleSheet("")
        self.faceOptimize_Button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/faceOptimize.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.faceOptimize_Button.setIcon(icon4)
        self.faceOptimize_Button.setIconSize(QtCore.QSize(151, 71))
        self.faceOptimize_Button.setObjectName("faceOptimize_Button")
        self.moreRiggingTools_Button = QtGui.QPushButton(self.groupBox)
        self.moreRiggingTools_Button.setEnabled(True)
        self.moreRiggingTools_Button.setGeometry(QtCore.QRect(330, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moreRiggingTools_Button.sizePolicy().hasHeightForWidth())
        self.moreRiggingTools_Button.setSizePolicy(sizePolicy)
        self.moreRiggingTools_Button.setStyleSheet("")
        self.moreRiggingTools_Button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/moreTools.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moreRiggingTools_Button.setIcon(icon5)
        self.moreRiggingTools_Button.setIconSize(QtCore.QSize(151, 71))
        self.moreRiggingTools_Button.setObjectName("moreRiggingTools_Button")
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 200, 491, 181))
        self.groupBox_2.setStyleSheet("font: italic 14pt \"Brush Script MT\";")
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.IKFKSwitch_Button = QtGui.QPushButton(self.groupBox_2)
        self.IKFKSwitch_Button.setGeometry(QtCore.QRect(10, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IKFKSwitch_Button.sizePolicy().hasHeightForWidth())
        self.IKFKSwitch_Button.setSizePolicy(sizePolicy)
        self.IKFKSwitch_Button.setStyleSheet("")
        self.IKFKSwitch_Button.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/IKFKSwitch.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.IKFKSwitch_Button.setIcon(icon6)
        self.IKFKSwitch_Button.setIconSize(QtCore.QSize(151, 71))
        self.IKFKSwitch_Button.setObjectName("IKFKSwitch_Button")
        self.mocapConvert_Button = QtGui.QPushButton(self.groupBox_2)
        self.mocapConvert_Button.setGeometry(QtCore.QRect(170, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mocapConvert_Button.sizePolicy().hasHeightForWidth())
        self.mocapConvert_Button.setSizePolicy(sizePolicy)
        self.mocapConvert_Button.setStyleSheet("")
        self.mocapConvert_Button.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/mocapConvert.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mocapConvert_Button.setIcon(icon7)
        self.mocapConvert_Button.setIconSize(QtCore.QSize(151, 71))
        self.mocapConvert_Button.setObjectName("mocapConvert_Button")
        self.poseDesigner_Button = QtGui.QPushButton(self.groupBox_2)
        self.poseDesigner_Button.setEnabled(True)
        self.poseDesigner_Button.setGeometry(QtCore.QRect(330, 20, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poseDesigner_Button.sizePolicy().hasHeightForWidth())
        self.poseDesigner_Button.setSizePolicy(sizePolicy)
        self.poseDesigner_Button.setStyleSheet("")
        self.poseDesigner_Button.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icon/poseDesigner.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.poseDesigner_Button.setIcon(icon8)
        self.poseDesigner_Button.setIconSize(QtCore.QSize(151, 71))
        self.poseDesigner_Button.setObjectName("poseDesigner_Button")
        self.buildPose_Button = QtGui.QPushButton(self.groupBox_2)
        self.buildPose_Button.setEnabled(True)
        self.buildPose_Button.setGeometry(QtCore.QRect(10, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildPose_Button.sizePolicy().hasHeightForWidth())
        self.buildPose_Button.setSizePolicy(sizePolicy)
        self.buildPose_Button.setStyleSheet("")
        self.buildPose_Button.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icon/buildPose.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buildPose_Button.setIcon(icon9)
        self.buildPose_Button.setIconSize(QtCore.QSize(151, 71))
        self.buildPose_Button.setObjectName("buildPose_Button")
        self.animFixShapeButton = QtGui.QPushButton(self.groupBox_2)
        self.animFixShapeButton.setEnabled(True)
        self.animFixShapeButton.setGeometry(QtCore.QRect(170, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.animFixShapeButton.sizePolicy().hasHeightForWidth())
        self.animFixShapeButton.setSizePolicy(sizePolicy)
        self.animFixShapeButton.setStyleSheet("")
        self.animFixShapeButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icon/animFixShape.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.animFixShapeButton.setIcon(icon10)
        self.animFixShapeButton.setIconSize(QtCore.QSize(151, 71))
        self.animFixShapeButton.setObjectName("animFixShapeButton")
        self.other_Button_7 = QtGui.QPushButton(self.groupBox_2)
        self.other_Button_7.setEnabled(False)
        self.other_Button_7.setGeometry(QtCore.QRect(330, 100, 151, 71))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.other_Button_7.sizePolicy().hasHeightForWidth())
        self.other_Button_7.setSizePolicy(sizePolicy)
        self.other_Button_7.setStyleSheet("")
        self.other_Button_7.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icon/Others.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.other_Button_7.setIcon(icon11)
        self.other_Button_7.setIconSize(QtCore.QSize(151, 71))
        self.other_Button_7.setObjectName("other_Button_7")
        advancedSkeletonWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(advancedSkeletonWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 512, 23))
        self.menubar.setObjectName("menubar")
        advancedSkeletonWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(advancedSkeletonWin)
        self.statusbar.setObjectName("statusbar")
        advancedSkeletonWin.setStatusBar(self.statusbar)

        self.retranslateUi(advancedSkeletonWin)
        QtCore.QMetaObject.connectSlotsByName(advancedSkeletonWin)

    def retranslateUi(self, advancedSkeletonWin):
        advancedSkeletonWin.setWindowTitle(QtGui.QApplication.translate("advancedSkeletonWin", "AdvancedSkeleton 5", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("advancedSkeletonWin", "Rigging Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("advancedSkeletonWin", "Animation Tools", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc