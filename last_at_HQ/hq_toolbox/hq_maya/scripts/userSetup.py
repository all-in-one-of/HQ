import sys, os
hq_root = os.getenv('hq_toolbox').replace( '\\', '/' )

ICONDIRS = (
    "D:/Users/Administrator/Documents/qs/hq_toolbox/hq_icons",
    "//10.99.1.6/Digital/Library/hq_toolbox/hq_icons"
)

sys.path.insert( 0,
                 os.path.join( hq_root, "hq_maya/hq_maya" ).replace('\\', '/')
                 )

import json
import maya.OpenMaya as om
import maya.mel as mel
import pymel.core as pm

import qsMaya as qm
from qsMainWin import *
import window as qmw


hq_libsPath = os.path.join( hq_root, 'hq_libs').replace( '\\', '/' )
sys.path.append( hq_libsPath )


qm.shelfTo2013Version( )
qm.copy_shelves( os.path.join( hq_root, "hq_maya/shelves")  )
qm.evalmels( os.path.join(hq_root, "hq_maya/scripts/evalMels") )


#print hq_libsPath, '\n', shelvesPath

