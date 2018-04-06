# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
from functools import partial

import time
class w20_intermediateObjects(object):
    _menuStr = '''{'path':'Pipeline Cache/Alembic/w20_intermediateObjects( )',
'icon':':/eye.png',
'tip' : '用中间对象属性隐藏物体',
'html':True,
'usage':"""
#优化选择的组中的物体，减少导出abc文件的大小
#其实将一个物体的intermediateObject属性设置为1，这个物体就不会被导出
#使用方法：选择物体或组
$fun( )""",
}
'''
    def __init__(self):
        self._withOutAttrs = ('shaveData', 'hairData', 'shaveObjId' )
        windowName = 'w20_intermediateObject_Objects'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        cmds.window(windowName, title=windowName, sizeable=False)
        cmds.columnLayout("w20_L01", p=windowName, adj=True)
        cmds.separator( height=15, style='in' )
        cmds.checkBoxGrp( 'w20_uiTypes', numberOfCheckBoxes=4, h=40, label='Object Types:   ', labelArray4=['mesh', 'nurbsSurface', 'nurbsCurve','locator'] )
        cmds.button( 'w20_uiHideTypes', p="w20_L01", label="Hide", h=40, c=self.w20_hideObjs_cmds  )
        cmds.separator( height=30, style='in' )
        self._progressControl = cmds.progressBar(p="w20_L01", h=10)
        cmds.button( 'w20_uiInvisible', p="w20_L01", label="Intermediate Invisible", h=40, c=partial( self.hide_intermediateObjects, invisible=True) )
        cmds.separator( height=30, style='in' )
        cmds.button( 'w20_uiHideEmptyGrps', p="w20_L01", label="Intermediate Empty Groups", h=40, c=self.intermediateEmptyGroups )
        cmds.showWindow(windowName)

    def _hasAttrs(self, *args):
        for attr in self._withOutAttrs:
            if cmds.attributeQuery( attr, node=args[0], exists=True):
                return True
        else:
            return False


    def w20_hideObjs_cmds(self, *args):
        msh = cmds.checkBoxGrp( 'w20_uiTypes', q=True, v1=True)
        sur = cmds.checkBoxGrp( 'w20_uiTypes', q=True, v2=True)
        cur = cmds.checkBoxGrp( 'w20_uiTypes', q=True, v3=True)
        loc = cmds.checkBoxGrp( 'w20_uiTypes', q=True, v4=True)
        self.hide_intermediateObjects(mesh=msh, nurbsSurface=sur, nurbsCurve=cur, locator=loc)


    def hide_intermediateObjects(self, *args, **kwargs):
        types = []
        if kwargs.get('mesh', False):
            types.append( 'mesh' )

        if kwargs.get( 'nurbsSurface', False):
            types.append( 'nurbsSurface' )

        if kwargs.get( 'nurbsCurve', False):
            types.append( 'nurbsCurve' )

        if kwargs.get('locator', False):
            types.append( 'locator' )

        if kwargs.get( 'invisible', False):
            objs =[ obj for obj in cmds.listRelatives( cmds.ls(sl=True), ad=True, type=['mesh', 'nurbsSurface', 'nurbsCurve','locator'], f=True) if not cmds.getAttr( obj+".intermediateObject") ]
            objs = set(objs)
            visibleObjs = set()
            start, end = int(cmds.playbackOptions(q=True, min=True)), int( cmds.playbackOptions(q=True, max=True) )
#            objs = cmds.ls( objs, invisible=True, l=True)
#            canotHidden = set()
#            for hobj in objs:
#                if self._hasAttrs(hobj):
#                    cmds.setAttr( hobj+'.intermediateObject', False)
#                    canotHidden = canotHidden.union( [hobj.rsplit( '|', i)[0] for i in range(hobj.count('|') ) ][1:] )
#                    continue
            cmds.progressBar(self._progressControl, e=True, maxValue= len(objs) )
            for frame in range(start, end+1):
                for hobj in objs:
                    children = [hobj.rsplit( '|', i)[0] for i in range(hobj.count('|') ) ]
                    for tf in children:
                        if not cmds.getAttr( tf+'.visibility', time=frame ) or cmds.getAttr( tf +'.intermediateObject'):
                            break
                    else:
                        visibleObjs.add( hobj )
                        cmds.progressBar(self._progressControl, e=True, step=1 )
                objs = objs.difference( visibleObjs )

                if len(objs)==0:
                    break
            [cmds.setAttr(obj+".intermediateObject", True) for obj in objs]
            print "%s objects was hid "% ( len( objs ) )
            cmds.progressBar( self._progressControl, e=True, endProgress=True)


        if types:
            objs =[ obj for obj in cmds.listRelatives( cmds.ls(sl=True), ad=True, type=types, f=True) if not cmds.getAttr( obj+".intermediateObject") ]
            for hobj in objs:
                if self._hasAttrs(hobj):
                    cmds.setAttr( hobj+'.intermediateObject', False)
                    break
                else:
                    cmds.setAttr( hobj+".intermediateObject", True)


    def intermediateEmptyGroups(self, objs=None):


        def intermediateEmptyGrp(obj ):
            objs01 = cmds.listRelatives(obj, type='transform', f=True)
            if not objs01:
                return
            for child in objs01:
                children = cmds.listRelatives( child, ad=True, type=['pfxHair', 'surfaceShape','nurbsCurve'], noIntermediate=True, f=True)
                if not children or not [sechild for sechild in children  if not cmds.getAttr( sechild+".intermediateObject") ]:
                    #print child
                    cmds.setAttr( child+".intermediateObject", True)
                else:
                    intermediateEmptyGrp(child)
        if not objs:
            objs = cmds.ls(sl=True)
        if not objs:
            raise IOError("Select a objects!")

        for obj in objs:
            if not cmds.listRelatives( obj, ad=True, type=['pfxHair', 'surfaceShape','nurbsCurve'], noIntermediate=True, f=True):
                cmds.setAttr( obj+'.intermediateObject', True)
                continue
            intermediateEmptyGrp( obj )