# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################


import maya.cmds as cmds
from qsMaya.utility import nameToNode
import maya.api.OpenMaya as newom
import qsMaya as qm
from functools import partial



class w18_transferMaterials(object):    
    _menuStr = '''{'path':'Rendering/Lighting Shading/w18_transferMaterials( )',
'icon':':/camera.svg',
'tip' : '物体的分组及材质的传递',
'usage':'w18_transferMaterials( )',
}
'''
    def __init__(self):
        self.w18_meshData = ()      
        windowName = 'w18_TransferMaterials'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        cmds.window(windowName, title=windowName, sizeable=1)
        cmds.columnLayout("w18_L01", p=windowName, adj=True)
        cmds.button( 'w18_uiReset', p="w18_L01", label="Get Selected", h=40, c= self.w18_addDataToList )
        cmds.textScrollList( 'w18_objsList', p="w18_L01", numberOfRows=8, allowMultiSelection=True, bgc=[.2,.2,.2], showIndexedItem=4, h=400,dcc=self.w18_itemDoubleClick  )
        cmds.button( 'w18_uiSetChange', p="w18_L01", label="Select Matched", h=40, c=self.w18_selectMatch  )
        cmds.separator( height=20, style='in' )
        cmds.button( 'w18_Transfer', p="w18_L01", label="Transfer Materials", h=40, c=self.doTransfer   )
        cmds.showWindow(windowName)

    
    def doTransfer(self):
        self.w18_selectMatch()
        qm.transferMaterials()
    
    def w18_getMeshData(self, *args):
        objs = cmds.ls(sl=True)
        allObjs = [ mesh for mesh in cmds.listRelatives( objs, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]
        objsData = {}
        
        #print 'new'
        
        for mesh in allObjs:
            omMesh = nameToNode( mesh )
            uv = None if cmds.polyEvaluate(mesh, uvcoord=True)==0 else newom.MFnMesh( omMesh ).getPolygonUV(0, 0 )
            key = str( cmds.polyEvaluate( mesh, vertex=True, edge=True, face=True) ) + str( uv )
            if not objsData.has_key( key ):
                objsData[key] = []
            objsData[key].append( mesh )
    
        #keysData = [  ( len(v),   '....' if len(v)>1 else v[0],  k )   for k, v in objsData.items()  ]
        keysData = []
        for k, v in objsData.items():
            v2 = 'Empty uvs' if k.endswith('None') else ''
            v2 = v2+'  ....'  if len(v)>1  else v2+v[0]
    
            keysData.append(  ( len(v), v2, k )   )
    
        keysData.sort( reverse=True)        
        self.w18_meshData = (objsData, keysData)
    
    
    
    def w18_addDataToList(self, *args):
        self.w18_getMeshData()
        cmds.textScrollList( 'w18_objsList', e=True, removeAll=True )
        cmds.textScrollList( 'w18_objsList', e=True, append=[ str(obj[0])+'\t'+obj[1] for obj in self.w18_meshData[1] ]  )
    
    
    def w18_selectMatch(self, *args):
        obj = cmds.ls(sl=True)
        mesh = [ mesh for mesh in cmds.listRelatives( obj, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]
    
        omMesh = nameToNode( mesh[0] )
        uv = newom.MFnMesh( omMesh ).getPolygonUV(0, 0 )
        key = str( cmds.polyEvaluate( mesh, vertex=True, edge=True, face=True) ) + str( uv )
    
        if self.w18_meshData[0].has_key( key ):
            cmds.select( self.w18_meshData[0][key], r=True )
            cmds.select( obj, add=True)
            index = [v[2] for v in self.w18_meshData[1]].index( key )+1
            cmds.textScrollList( 'w18_objsList', e=True, deselectAll=True, selectIndexedItem=index)
            cmds.textScrollList( 'w18_objsList', e=True, selectIndexedItem=index)
    
    
    
    def w18_itemDoubleClick(self, *args):
        itemIndex = cmds.textScrollList( 'w18_objsList', q=True, selectIndexedItem=True)[0]
        key = self.w18_meshData[1][itemIndex-1][2]
        objs = self.w18_meshData[0][key]
        cmds.select( objs, r=True)






class w18_A_transferMaterials(object):
    _menuStr = '''{'path':'Rendering/Lighting Shading/w18_A_transferMaterials( )',
'icon2':'render_lambert.png',
'html':True,
'usage':"""
#选择有材质物体，点From Object;
#选择要被传递的物体，点To Objects;
#点击Transfer Materials，进行材质的传递
$fun( )""",
}
'''
    def __init__(self):
        self.fromObjs = []
        self.toObjs = []            
        windowName = 'w18_A_TransferMaterials'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        cmds.window(windowName, title=windowName, sizeable=1)
        cmds.columnLayout("w18_A_L01", p=windowName, adj=True)
        cmds.button( 'w18_A_uiFrom', p="w18_A_L01", label="From Objects", h=40, c=self.getFromObjs )
        cmds.button( 'w18_A_uiTo', p="w18_A_L01", label="To Objects", h=40, c=self.getToObjs )
        cmds.separator( height=20, style='in' )
        cmds.button( 'w18_A_Transfer', p="w18_A_L01", label="Transfer Materials", h=40, c=self.doTransfer  )
        cmds.showWindow(windowName)
    
    def getFromObjs(self, *args):
        self.fromObjs = cmds.ls(sl=True)
    
    def getToObjs(self, *args):
        self.toObjs = cmds.ls(sl=True)
        
        
    def doTransfer(self, *args):
        print self.fromObjs, self.toObjs
        qm.w18_A_transferMaterials_cmd( self.fromObjs, self.toObjs)



