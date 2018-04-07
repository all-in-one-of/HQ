'''
@name:          coopQt.py
@repository:    https://github.com/studiocoop/maya
@version:       0.*
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Maya coop qt library

@requires:      -

@run:           import coopQt as cqt (suggested)

@created:       12 Aug, 2015
@change:    29 Apr, 2017
'''
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMayaUI as omUI
from Qt import QtCore, QtGui, QtWidgets
try:
	from shiboken import wrapInstance
except:
	from shiboken2 import wrapInstance

#STYLES
fontHeader = QtGui.QFont('MS Shell dlg 2', 15);
fontFooter = QtGui.QFont('MS Shell dlg 2', 8);
# STYLING
#button.setStyleSheet("background-color: rgb(0,210,255); color: rgb(0,0,0);")
#imagePath = cmds.internalVar(upd = True) + 'icons/background.png')
#button.setStyleSheet("background-image: url(" + imagePath + "); border:solid black 1px;")
#self.setStyleSheet("QLabel { color: rgb(50, 50, 50); font-size: 11px; background-color: rgba(188, 188, 188, 50); border: 1px solid rgba(188, 188, 188, 250); } QSpinBox { color: rgb(50, 50, 50); font-size: 11px; background-color: rgba(255, 188, 20, 50); }")


#WINDOW
def getMayaWindow():
    ptr = omUI.MQtUtil.mainWindow() #pointer to main window
    return wrapInstance(long(ptr), QtWidgets.QWidget) #wrapper

class mayaUI(QtWidgets.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(mayaUI, self).__init__(parent)

def createMayaWindow(title, new, brand='studio.coop', tooltip='introduction to the UI'):
    if cmds.window(title, exists=True):
        if not new:
            cmds.showWindow(title)
            return None, True
        cmds.deleteUI(title, wnd=True) #delete old window
    mWindow = mayaUI()
    mWindow.setWindowTitle(title)
    mWindow.setObjectName(title)
    mWindow.setWindowFlags(QtCore.Qt.Tool) #always on top (multiplatform)

    # Default UI elements
    ''' Create the widgets for the dialog '''
    mWindow.header = QtWidgets.QLabel(title)
    mWindow.header.setAlignment(QtCore.Qt.AlignHCenter)
    mWindow.header.setFont(fontHeader)
    mWindow.header.setContentsMargins(10, 10, 10, 10)

    mWindow.brand = QtWidgets.QLabel(brand)
    mWindow.brand.setToolTip(tooltip)
    mWindow.brand.setStyleSheet("background-color: rgb(40,40,40); color: rgb(180,180,180); border:solid black 1px")
    mWindow.brand.setAlignment(QtCore.Qt.AlignHCenter)
    mWindow.brand.setGeometry(10, 10, 20, 20)
    mWindow.brand.setFont(fontFooter)
    print "window successfully created"
    return mWindow, False


def getCoopIconPath():
    """
    :returns coop icon path directory
    """
    iconPaths = mel.eval('getenv("XBMLANGPATH")')
    for iconPath in iconPaths.split(';'):
        if "coop/maya/icons" in iconPath:
            return iconPath


def labeledComboBox(label, options):
    """
    :TODO Convert to CLASS
    Creates and returns a labeled combobox

    :param label: String containing label text
    :param options: List of options to display in combo box e.g. ['.png', '.jpg', '.tif']
    :returns A labeled combo box
    """
    w = QtWidgets.QWidget()
    wLayout = QtWidgets.QHBoxLayout()
    labelW = QtWidgets.QLabel(label)
    comboW = QtWidgets.QComboBox()
    comboW.addItems(options)
    wLayout.addWidget(labelW)
    wLayout.addWidget(comboW)
    w.setLayout(wLayout)
    return w


class iconButton(QtWidgets.QLabel):
    """
    Icon Button class object (extended from QLabel)

    :param image: String -> relative image path ("images/butIcon.png")
    :param tooltip: String -> tooltip of button (default -> "")
    :param size: List of unsigned integers -> size of button in pixels (default -> [25, 25])
    :param parent: Object -> parent object (default -> None)
    """
    clicked = QtCore.Signal(str)

    def __init__(self, image, tooltip='', size=[25,25], parent=None):
        super(iconButton, self).__init__(parent)
        self.setFixedSize(size[0],size[1])
        self.setScaledContents(True)
        self.setToolTip(tooltip)
        self.setPixmap(image)

    def mouseReleaseEvent(self, event):
        self.clicked.emit("emit the signal")


class widgetGroup(QtWidgets.QWidget):
    """
    Simple widget group class object with embedded layout and batch widget assignment

    :param qWidgets: QWidget object array -> widgets to group (default -> [])
    :param qLayout: QtWidgets Layout object -> layout of group (default -> QtWidgets.QVBoxLayout())
    :param parent: QtWidgets object -> parent QtWidgets object (default -> None)

    :def addWidget(widget): QtWidgets object -> widget to be added
    :def addWidgets(widgets): List of QtWidgets objects -> widgets to be added
    """
    def __init__(self, qWidgets=[], qLayout=QtWidgets.QVBoxLayout(), parent=None):
        super(widgetGroup, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
        self.groupLayout = qLayout
        self.groupLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.groupLayout)
        for widget in qWidgets:
            self.groupLayout.addWidget(widget)

    def addWidget(self, widget):
        self.groupLayout.addWidget(widget)

    def addWidgets(self, widgets):
        for widget in widgets:
            self.groupLayout.addWidget(widget)
