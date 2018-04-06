# -*- coding: utf-8 -*-
import maya.cmds as cmds

def w21_checkObjectSetOfShaveHair(): 
    
    windowName = 'w21_checkObjectSetOfShaveHair'        
    if cmds.window( windowName, exists=True):
        cmds.deleteUI( windowName)
    sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0] 
    cmds.window(windowName, title=windowName, sizeable=True)
    cmds.formLayout("w21_layout", p=windowName)    
    cmds.textScrollList( 'w21_hair', p="w21_layout", allowMultiSelection=True, en=0, bgc=[0,0,0], showIndexedItem=4, doubleClickCommand='w21_doubleClick_cmd()')
    cmds.formLayout( 'w21_layout', edit=True, attachForm=[('w21_hair', 'top', 5), ('w21_hair', 'bottom', 5), ('w21_hair', 'left', 5),('w21_hair', 'right', 5)] )    
    cmds.showWindow(windowName)
    
    #hairs = cmds.ls( exactType=['shaveHair','hairSystem'], l=True)    
    hasNotSet = []    
    for shave in cmds.ls( exactType='shaveHair'):
        if not cmds.listConnections( shave+'.growthSet', d=False, shapes=True):
            hasNotSet.append( shave )

    
    cmds.textScrollList('w21_hair', e=True, en=True, removeAll=True)
    for shave in hasNotSet:
        cmds.textScrollList('w21_hair', e=True, append=shave)    
    

def w21_doubleClick_cmd():
    item = cmds.textScrollList( 'w21_hair', q=True, selectItem=True)
    cmds.select( item, r=True)