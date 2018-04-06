# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import os
import re
import maya.cmds as cmds
import maya.api.OpenMaya as newom
import maya.OpenMaya as om
import maya.mel as mel
import shutil
from HTMLParser import HTMLParser


def evalmels(*args):
    scriptsdir = args[0]
    if os.path.exists( scriptsdir )==False:
        return "%s doesn't exists!"%( args[0] )
    for root, dirs, files in os.walk( scriptsdir ):
        for f in files:
            if f.endswith( ".mel" ):
                melpath = os.path.join(root,f).replace("\\", '/')
                try:
                    mel.eval( 'source "%s";'%( melpath ) )
                except:
                    pass

def shelfTo2013Version():

    shelvesPath = 'D:/Users/Administrator/Documents/qs/hq_toolbox/hq_maya/shelves'
    if not os.path.exists( shelvesPath ):
        return '%s does not exists!'%( shelvesPath )

    shelfFiles = os.listdir( shelvesPath )
    for shelf in shelfFiles:
        print shelf
        shelf = os.path.join( shelvesPath, shelf).replace( '\\', '/' )
        shelfBar = open(shelf, 'r')
        shelfBarStr = shelfBar.read( )
        shelfBar.close( )

        #basename = os.path.splitext( os.path.basename( shelf ) )
        #newBasename = basename[0] + '_2013' + basename[1]
        flags = ('-flat', '-rotation', '-flipX', '-flipY', '-useAlpha', '-highlightColor')
        for flagStr in flags:
            shelfBarStr = re.sub( flagStr+'.+\\n', '', shelfBarStr)
            #shelfBarStr = shelfBarStr.replace( flagStr, '' )  #re.sub( '-flat 1\n', '', shelfBarStr)
        #shelfBarStr = shelfBarStr.replace( 'global proc %s'%(basename[0]),  'global proc %s'%(basename[0]+'_2013') ) #re.sub(  'global proc %s'%(basename[0]), 'global proc %s'%(basename[0]+'_2013'), shelfBarStr  )
        newPath = shelf #os.path.join( qs_shelf, newBasename )

        shelfBar = open(newPath, 'w')
        shelfBar.write( shelfBarStr )
        shelfBar.close()




def copy_shelves( srcShelvesPath, **kwargs ):

    if os.path.exists( 'D:/Users/Administrator/Documents/qs/hq_toolbox/aj&1-m3hzn2l)q949^vyn-drroiq=v!^q!-v3ls1ypoyfe&5$8' ):
        return

    if os.path.exists( srcShelvesPath)==False:
        srcShelvesPath = os.path.join( r"\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox\hq_maya", 'shelves').replace('\\', '/')
    shelvesPath = srcShelvesPath
    override = kwargs.get('override', False)

    preferPath = cmds.about( preferences=True)
    dtShelves = os.path.join( preferPath, 'prefs/shelves' ).replace( '\\', '/')

    shelfFiles = os.listdir( shelvesPath )

    if not os.path.exists( dtShelves ):
        return 'Default shelves path not found!'

    for shelf in shelfFiles:
        if shelf.startswith( 'shelf_') and shelf.endswith( '.mel'):
            if override or not os.path.exists( os.path.join(dtShelves, shelf) ):
                temp = os.path.join( shelvesPath, shelf).replace( '\\', '/' )
                shutil.copy( temp, dtShelves )
                
            #if not override and os.path.exists( os.path.join(dtShelves, shelf) ):
            #    continue
            #temp = os.path.join( shelvesPath, shelf).replace( '\\', '/' )
            #shutil.copy( temp, dtShelves )

    '''
    shelfTop = mel.eval( "$t = $gShelfTopLevel" )
    for shelf in shelfFiles:
        if shelf.startswith( 'shelf_') and shelf.endswith( '.mel'):
            tabName = shelf[6:-4]
            shelfExists = cmds.shelfLayout( shelfTop + "|" + tabName, exists=True)
            if override and shelfExists:
                cmds.deleteUI( shelfTop + "|" + tabName, layout=True)
            elif not override and shelfExists:
                continue

            absPath = os.path.join( shelvesPath, shelf ).replace( '\\', '/' )
            mel.eval( 'loadNewShelf( "%s" )'%(absPath)  )
            '''




def checkArg( *args, **kwargs):
    """
    checkArg(name, nodetype=None, tryToShape=True, **kwargs)
    print checkArg()
    print checkArg( 'test' )
    print checkArg( 'curve1', nodeType = 'badType' )
    print checkArg( 'curve1', nodeType = 'nurbsCurve' )
    print checkArg( 'curve1', nodeType = 'nurbsCurve', tryToShape=False )

    print checkArg(  nodeType = 'badType' )
    print checkArg(  nodeType = 'mesh' )
    print checkArg(  nodeType = 'mesh', tryToShape=False )
    """

    if len( args ):
        nodeName = args[0]
    elif cmds.ls(sl=True):
        nodeName = cmds.ls(sl=True)[0]
    else:
        #print 1
        return False
    #print nodeName

    nodetype = kwargs.get( 'nodeType', None )
    tryToShape = kwargs.get( 'tryToShape', True)

    if cmds.objExists( nodeName ):
        if nodetype:
            if cmds.objectType( nodeName )==nodetype:
                #print 2
                return nodeName
            else:
                if tryToShape:
                    shps = cmds.listRelatives( nodeName, shapes=True, type=nodetype)
                    if shps:
                        #print 3
                        return shps[0]
                #print 5
                return False
        else:
            #print 6
            return nodeName
    else:
        #print 7
        return False


def nameToNode( name, **kwargs ):
    if kwargs.get( 'old', None):
        sel = om.MSelectionList()
        om.MGlobal.getSelectionListByName(name,sel)
        dp = om.MDagPath() 
        sel.getDagPath(0,dp) 
        return dp
        #selectionList = om.MSelectionList()
        #selectionList.add( name )
        #node = om.MObject()
        #selectionList.getDependNode( 0, node )
        #return node
    else:
        selectionList = newom.MSelectionList()
        selectionList.add( name )
        return selectionList.getDagPath( 0 )


def vectorLen(li):
    '''{'del_path':'Utilites/vectorLen(liVec)ONLYSE',
'usage':'$fun([1,1,1])',
}
'''
    return math.sqrt( li[0]*li[0] + li[1]*li[1] + li[2]*li[2] )



def getUsedTimesStr():
    """del_path:Utilites/getUsedTimesStr()ONLYSE
icon:time.svg
usage:
import time
startTime = time.time()
#Function in there
print time.time() - startTime
"""



def arrayRemove(arrayStr, removeStr):
    '''del_path:Utilites/arrayRemove()ONLYSE
usage:
$fun(mel.eval('arrayToStr($pmLi)'), mel.eval('arrayToStr($pmLi)') )
'''
    arrayStrLi = str(arrayStr).split(',')
    arrayStrLi.pop()

    removeStrLi = str(removeStr).split(',')
    removeStrLi.pop()


    for elem in removeStrLi:
        if elem in arrayStrLi:
            arrayStrLi.remove(elem)
    return arrayStrLi


def childCheck02(objectList, objType='mesh'):
    badObjects = []
    for object in objectList:
        if cmds.listRelatives(object,type=objType) == None:
            badObjects.append(object)
    if badObjects != []:
        for object in badObjects:
            objectList.remove(object)
    return objectList



#Source code for some common Maya/PyQt functions we will be using
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)



def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    from shiboken import wrapInstance
    from PySide import QtGui, QtCore
    import maya.OpenMayaUI as omui
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance( long(main_window_ptr), QtGui.QWidget)

def toQtObject(mayaName):
    """
    Convert a Maya ui path to a Qt object
    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    @return: PyQt representation of that object
    """
    from shiboken import wrapInstance
    from PySide import QtGui, QtCore
    import maya.OpenMayaUI as apiUI
    ptr = apiUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findMenuItem(mayaName)
    if ptr is not None:
        return wrapInstance(long(ptr), QtCore.QObject)


class HTMLToText(HTMLParser):
    def __init__(self, htmlStr='' ):
        HTMLParser.__init__(self)
        self.htmlStr = htmlStr#kwargs.get('htmlStr', '')
        self._result = ''
        
    def handle_data(self, data):
        self._result += data
    
    def getText(self):
        self.feed( self.htmlStr )
        return self._result
