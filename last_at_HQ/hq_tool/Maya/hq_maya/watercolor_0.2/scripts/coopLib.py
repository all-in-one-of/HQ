'''
@name:          coopLib.py
@repository:    https://github.com/studiocoop/maya
@version:       0.*
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Maya coop python library

@requires:      coopRestart

@run:           import coopLib as lib (suggested)

@created:       05 May, 2015
@change:        12 Jul, 2016
'''
import os
import sys
import subprocess
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
######################################################################################
#GENERAL UTILITIES
######################################################################################
def checkAboveVersion(year):
    '''checks if Maya is above version $year'''
    mVersion = cmds.about(v=True)
    mVersion = int(mVersion.split()[0])
    if (mVersion > year):
        return True
    return False

def getEnvDir():
    '''returns environment dir'''
    envDir = os.path.abspath(cmds.about(env=True, q=True))
    return os.path.dirname(envDir)

def getLibDir():
    '''returns directory of the library'''
    return os.path.dirname(os.path.realpath(__file__))

def openUrl(url):
    '''opens url in browser'''
    import webbrowser
    webbrowser.open(url, new=2, autoraise=True)

def restartMaya(brute=True):
    '''force restart maya (use restartDialog)'''
    if not brute:
        mayaPyDir = os.path.join(os.path.dirname(sys.executable), "mayapy")
        if cmds.about(nt=True, q=True):
            mayaPyDir += ".exe"
        scriptDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "coopRestart.py")
        print scriptDir
        subprocess.Popen([mayaPyDir, scriptDir])
        cmds.quit(force=True)
    else:
        os.execl(sys.executable, sys.executable, * sys.argv)

def restartDialog(brute=True):
    restart = cmds.confirmDialog( title='Restart Maya',
                message='Maya needs to be restarted in order to show changes\nWould you like to restart maya now?',
                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No', ma='center' )
    if restart == 'Yes':
        restartMaya(brute)


######################################################################################
#MAYA UTILITIES
######################################################################################
def createEmptyNode(inputName):
    '''creates a completely empty node with $inputName'''
    cmds.select(cl=True)
    cmds.group( em=True, name=inputName )
    nodeName = cmds.ls(sl=True)
    keyableAttributes = cmds.listAttr(nodeName, k=True )
    for attribute in keyableAttributes:
        cmds.setAttr('{0}.{1}'.format(nodeName[0], attribute), l=True, k=False)


def deleteShelf():
    if cmds.shelfLayout('CurvesSurfaces', q=True, ex=True):
        cmds.deleteUI('CurvesSurfaces', layout=True)


def getActiveModelPanel():
    '''gets the string of the active model editor panel (3D viewport returns none if none is active'''
    activePanel = cmds.getPanel(wf=True);
    if cmds.getPanel(typeOf=activePanel)=='modelPanel':
        return activePanel
    else:
        return cmds.playblast(ae=True)


def deleteShelves(shelvesDict=None):
    '''delete shelves
    $shelves: dictionary of shelf name and mel file without prefix
    e.g. {"Animation" : "Animation.mel"}'''
    envDir = getEnvDir()
    if not shelvesDict:
        cmds.error('No shelf array given')
    #Maya creates all default shelves in prefs only after each has been opened (initialized)
    for shelf in shelvesDict:
        try:
            mel.eval('jumpToNamedShelf("{0}");'.format(shelf))
        except:
            continue
    mel.eval('saveAllShelves $gShelfTopLevel;') #all shelves loaded (save them)
    #time to delete them
    shelfTopLevel = mel.eval('$tempMelVar=$gShelfTopLevel') + '|'
    for shelf in shelvesDict:
        shelfLayout = shelvesDict[shelf].split('.mel')[0]
        if cmds.shelfLayout(shelfTopLevel + shelfLayout, q=True, ex=True):
            cmds.deleteUI(shelfTopLevel+shelfLayout, layout=True)
    #mark them as deleted to avoid startup loading
    shelfDir = os.path.join(envDir,'prefs','shelves')
    for shelf in shelvesDict:
        shelfName = os.path.join(shelfDir,'shelf_' + shelvesDict[shelf])
        deletedShelfName = shelfName + '.deleted'
        if os.path.isfile(shelfName):
            #make sure the deleted file doesn't already exist
            if os.path.isfile(deletedShelfName):
                os.remove(shelfName)
                continue
            os.rename(shelfName,deletedShelfName)
    restartDialog()


def restoreShelves():
    '''restore deleted shelves'''
    scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
    envDir = os.path.dirname(scriptsDir)
    shelfDir = os.path.join(envDir,'prefs','shelves')
    for shelf in os.listdir(shelfDir):
        if shelf.endswith('.deleted'):
            restoredShelf = os.path.join(shelfDir, shelf.split('.deleted')[0])
            deletedShelf = os.path.join(shelfDir, shelf)
            #check if it has not been somehow restored
            if os.path.isfile(restoredShelf):
                os.remove(deletedShelf)
            else:
                os.rename(deletedShelf, restoredShelf)
    restartDialog()


'''Batch change attributes of selected objects e.g.
lib.changeAttributes(['jointOrientX', 'jointOrientY', 'jointOrientZ'], 0)
'''
def changeAttributes(attributes, value):
    selected = cmds.ls(sl=True)
    for sel in selected:
        for attribute in attributes:
            try:
                cmds.setAttr("{0}.{1}".format(sel, attribute), value)
            except:
                cmds.warning("There is an issue with {0}.{1}. The value {2} could not be set".format(sel, attribute, value))


'''Batch copy attributes of selected objects, e.g.
lib.copyAttributes(['jointOrientX', 'jointOrientY', 'jointOrientZ'])
'''
def copyAttributes(attributes):
    selected = cmds.ls(sl=True)
    if selected:
        source = selected.pop(0)
        for attribute in attributes:
            sourceValue = cmds.getAttr("{0}.{1}".format(source, attribute))
            for target in selected:
                try:
                    cmds.setAttr("{0}.{1}".format(target, attribute), sourceValue)
                except:
                    cmds.warning("There is an issue with {0}.{1}. The value {2} could not be set".format(target, attribute, sourceValue))

'''Snap targets to source
if not specified, the first selected object is considered as source, the rest as targets
Note: targets should not have their transformations freezed
'''
def snap(source='', targets=[], type="translation"):
    #check if there are source and targets defined/selected
    if not source:
        selected = cmds.ls(sl=True)
        if selected:
            source = selected.pop(0)
            if not targets:
                targets = selected
        else:
            cmds.error("No source specified or selected.")
    if not targets:
        targets = cmds.ls(sl=True)
    else:
        if isinstance(targets, basestring):
            targets = [targets]
    if not targets:
        cmds.error("No targets to snap defined or selected")

    #using xform brings pr
    #proceed to snap
    if type=="translation":
        worldTranslateXform = cmds.xform('{0}'.format(source), q=True, worldSpace=True, piv=True) #list with 6 elements
        for target in targets:
            cmds.xform('{0}'.format(target), worldSpace=True, t=(worldTranslateXform[0], worldTranslateXform[1], worldTranslateXform[2]))
        print "Translation snapped",

    if type=="rotation":
        sourceXform = cmds.xform('{0}'.format(source), q=True, worldSpace=True, ro=True)
        for target in targets:
            cmds.xform('{0}'.format(target), worldSpace=True, ro=(sourceXform[0], sourceXform[1], sourceXform[2]))
        print "Rotation snapped",

    if type=="position":
        sourcePos = cmds.xform('{0}'.format(source), q=True, worldSpace=True, piv=True) #list with 6 elements
        sourceRot = cmds.xform('{0}'.format(source), q=True, worldSpace=True, ro=True)
        for target in targets:
            cmds.xform('{0}'.format(target), worldSpace=True, t=(sourcePos[0], sourcePos[1], sourcePos[2]))
            cmds.xform('{0}'.format(target), worldSpace=True, ro=(sourceRot[0], sourceRot[1], sourceRot[2]))
        print "Position snapped",



######################################################################################
#PYSIDE UTILITIES
######################################################################################
#Convert .ui file to .py file
def uiToPy(path):
    from pysideuic import compileUi
    pyfile = open(path, 'w')
    compileUi("[path to input ui file]\makeCube.ui", pyfile, False, 4,False)
    pyfile.close()


######################################################################################
#MAYA PYTHON API
######################################################################################
#get MObject of node
def getMObject(node):
    selectionList = om.MSelectionList()
    selectionList.add(node)
    oNode = om.MObject()
    selectionList.getDependNode(0, oNode)
    return oNode
