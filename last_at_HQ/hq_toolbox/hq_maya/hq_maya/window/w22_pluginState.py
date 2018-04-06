# -*- coding: utf-8 -*-

import maya.cmds as cmds
from functools import partial

class w22_plguinState(object):
    _menuStr = '''{'delpath':'General/w22_plguinState( )',
'tip' : '检查必须要安装的插件',
'html':True,
'usage':"""
#检查必须要安装的插件有没有安装
$fun( )""",
}
'''
    RED = (.5, 0, 0)
    GREEN = (0, .5, 0)
    standardInfo = {2013:{ 'anzovinRigNodes.mll': ('1.0', '201300' ),
                              'mtoa.mll': ('1.0.0.1', 'Unknown'),
                              'vrayformaya.mll': ('2.40.01', '201300'),
                              'shaveNode.mll': ('1.1', '201300'),
                              'realflow.mll': ('2014.0.1', '201300' )
                              },
                    2015:{ 'anzovinRigNodes.mll': ('1.0','201500'),
                              'mtoa.mll': ('1.2.3.1', 'Unknown'),
                              'vrayformaya.mll': ('3.10.01', '201500'),
                              'shaveNode.mll': ('1.1', '201507'),
                              'realflow.mll': ('2014.0.1', '201500')
                              },
                        }
    
    def __init__(self):
        
        self.maya_version = int( cmds.about(v=True)[:4] )        
        windowName = 'w22_pluginState'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        
        cmds.window(windowName, title=windowName, sizeable=False )       
        
        if not self.standardInfo.has_key(self.maya_version):
            cmds.columnLayout()
            cmds.text( label='This script is not working for maya %d'%(self.maya_version) )
        else:
            cmds.rowColumnLayout( numberOfColumns=2, columnWidth=( (1,150), (2, 100)), rowSpacing=(1, 10), columnAlign=(2,'left') )     
            mllList = self.standardInfo[self.maya_version].keys()
            mllList.sort()
            
            for index, mll in enumerate( mllList ):
                ver = self.standardInfo[self.maya_version][mll][0]
                uimll = mll.replace('.', '_')
                cmds.checkBox( uimll, label=mll, bgc=\
                               self.GREEN if cmds.pluginInfo( mll, q=True, loaded=True) else self.RED,\
                               value=True if cmds.pluginInfo( mll, q=True, loaded=True) else False,\
                               changeCommand= partial( self.loadPlugin , mll),
                               )
                cmds.text( uimll+"_ver", label=ver, bgc=\
                           self.GREEN \
                           if cmds.pluginInfo( mll, q=True, loaded=True) and cmds.pluginInfo( mll, q=True, version=True)==ver \
                           else self.RED\
                           )
        
        cmds.showWindow()


    def loadPlugin(self, mll, *args):
        pluginState = cmds.pluginInfo( mll, q=True, loaded=True)        
        if pluginState:
            cmds.unloadPlugin(mll)
            self.setColour(mll)
        else:
            try:
                cmds.loadPlugin( mll )
                self.setColour(mll)
            except:
                self.setColour(mll)
                
    
    def setColour(self, mll):
        uimll = mll.replace('.', '_')        
        if cmds.pluginInfo( mll, q=True, loaded=True):
            curVer = cmds.pluginInfo( mll, q=True, version=True)
            curApiVer = cmds.pluginInfo( mll, q=True, apiVersion=True)
            vaildVer, vaildApiVer = self.standardInfo[self.maya_version][mll]
            
            cmds.checkBox( uimll, e=True, bgc=self.GREEN )            
            cmds.text( uimll+'_ver', e=True, bgc=\
                       self.GREEN if curVer==vaildVer and curApiVer==vaildApiVer else self.RED 
                       )
        else:
            cmds.checkBox( uimll, e=True, bgc=self.RED )
            cmds.text( uimll+'_ver', e=True, bgc=self.RED )