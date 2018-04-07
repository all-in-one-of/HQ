import sys
path='E:/work/7_0616_CheckNode'
if not path in sys.path:
    sys.path.append(path)

import checkNodeForMaya
import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken import wrapInstance
from PySide import QtCore, QtGui

class k_loadcheckNode(checkNodeForMaya.Communicate,checkNodeForMaya.checkNodes,checkNodeForMaya.k_replyNodes):
    def __init__(self):
    	
