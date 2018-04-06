# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds

#-------------------   w15_selFaceByAttrValue_win
class w15_selFaceByAttrValue_win(object):
    
    _menuStr = '''{'path':'Houdini/w15_selFaceByAttrValue_win()',
'icon':':/menuIconWindow.png',
'tip' : '用来选导入的houdini物体的面',
'usage':'$fun()',
}
'''
    
    def __init__(self):
        windowName = 'w15_selFaceByAttrValue_win'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
    
        cmds.window(windowName, title="w15 Select faces By attribute value", sizeable=0)
        cmds.columnLayout(adj=True)
        cmds.checkBox('w15_rename', l='Rename children', h=20, v=False, cc='cmds.textFieldGrp("w15_namePrefix", e=True,   enable=cmds.checkBox("w15_rename", q=True, v=True)  )'  )
        cmds.textFieldGrp( 'w15_namePrefix', label='Prefix', h=30, enable=False, text='piece' )
        cmds.separator(st='out', h=10)
        cmds.textFieldGrp( 'w15_attrName', label='Attribute Name', text='attribute1', h=30 )
        cmds.intFieldGrp( 'w15_value', label='Value', h=30, value1=0 )
        cmds.button(l='Select', h=40, c=self.w15_sel_cmd )
        cmds.separator(st='out', h=20)
        cmds.button(l='List empty uv set objects from selected', h=40, c=self.listEmptyUvsObjs )
        cmds.text( l='The polys does not have uv sets:', align='left', h=20)
        #cmds.frameLayout('w04_uiFrameSegLayout', label="Frame segments", collapsable=True,  borderStyle="in", collapse=True)
        cmds.textScrollList( 'w15_uiEmptyUVS', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, h=300,dcc=self.w15_doubleClicked )
        cmds.showWindow( windowName )
    
    def w15_doubleClicked(self, *args):
        selObjs = cmds.textScrollList("w15_uiEmptyUVS",q=True,selectItem=True)
        if selObjs:
            cmds.select( selObjs, r=True)
    
    
    def listEmptyUvsObjs(self, *args):
        cmds.textScrollList("w15_uiEmptyUVS",e=True,removeAll=True)
        
        objs = cmds.ls(sl=True)        
        emptyUVS = [obj for obj in objs if not cmds.polyUVSet( obj, q=True, allUVSets=True) or not cmds.polyEvaluate(obj, uvcoord=True)]
        cmds.textScrollList("w15_uiEmptyUVS",e=True,append=emptyUVS )

    
    
    
    def selFaceByAttrValue(self, dopGrp, attr, value, renameChildren=True, prefix='piece', *args):
        #attr = 'Cd'
        #value = (1,1,1)
        if renameChildren:
            objs = cmds.listRelatives(dopGrp, f=True)
            for obj in objs:
                newName = cmds.rename( obj, 'piece*')
                newShape = cmds.listRelatives( newName, shapes=True, type='mesh', f=True)[0]
                shapeName = newName.rsplit('|',1)[-1]
                cmds.rename( newShape, shapeName+'Shape')
    
        meshs = cmds.listRelatives(dopGrp, ad=True, type='mesh', f=True)
        matData = {}
        for mesh in meshs:
            cd = cmds.getAttr( '%s.%s'%(mesh,attr) )
            faceSet = []
            for i in range( len(cd) ):
                if cd[i] == value:
                    faceSet.append( i )
            matData[mesh] = faceSet
    
        beSel = []
        for key, value in matData.items():
            beSel.extend( ['%s.f[%d]'%(key,i) for i in value] )
    
        cmds.select( beSel, r=True)
    
    
    def w15_sel_cmd(self, *args):
        attr = str( cmds.textFieldGrp( 'w15_attrName', q=True, text=True) )
        value = cmds.intFieldGrp( 'w15_value', q=True, value1=True)
        dopGrp = cmds.ls(sl=True, exactType='transform', l=True)
        if dopGrp==None:
            raise IOError('Select a group!')
        renameChildren = cmds.checkBox("w15_rename", q=True, v=True)
        prefix = cmds.textFieldGrp( 'w15_namePrefix',  q=True, text=True)
        prefix = prefix if prefix!='' else 'piece'
        self.selFaceByAttrValue( dopGrp, attr, value, renameChildren, prefix )
        #print type(attr), type(value)
    #-----------w15 end
    
