# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
#-----------------------------------w05--------------------------------------------------
class w05_selectByMapWin(object):
    _menuStr = '''{'del_path':'Edit/w05_selectByMapWin()',
'icon':':/selectByObject.png',
'tip' : '用贴图选择物体',
'usage':'$fun()',
}
'''
        
    def __init__(self):
        self.w05_data = {}
        if cmds.window('w05', exists=True):
            cmds.deleteUI('w05')
        cmds.window('w05',title='w05_selectByMap', sizeable=False)
        cmds.columnLayout( 'w05_rl01', p='w05')
        cmds.textFieldGrp( 'w05_mapObj', label='mapObj', h=30, cc=self.w05_changeUI_cmd )
        cmds.textFieldGrp( 'w05_map', label='map', h=30, cc=self.w05_changeUI_cmd )
        
        cmds.button('w05_01', label='Get Objects From Selected', h=50, w=150, command="w05_data=w05_getData_cmd()\nw05_changeUI_cmd(w05_data)")
        cmds.floatSliderGrp( 'w05_02', field=True, label='luminance', minValue=0, maxValue=1, step=.01,h=40,cw3=[60,50,100], changeCommand=self.w05_changeUI_cmd )
        cmds.checkBox('w05_03', label='min', bgc=[0,.5,0], h=30, cc=self.w05_changeUI_cmd )
        cmds.checkBox('w05_04', label='man', bgc=[0,.5,0], h=30, cc=self.w05_changeUI_cmd ) 
        cmds.checkBox( 'w05_06', label='SELECT', bgc=[.5,0,0], h=50,rs=False, changeCommand=self.w05_changeUI_cmd )
        cmds.showWindow( 'w05')
    
    
    def w05_getData_cmd(self, *args):
        mapObj = cmds.textFieldGrp( 'w05_mapObj', q=True, text=True)
        if cmds.objExists(mapObj) == False:
            raise IOError('No found %s'%(mapObj) )
            
        map = cmds.textFieldGrp( 'w05_map', q=True, text=True)    
        if cmds.objExists(mapObj) == False:
            raise IOError('No found %s'%(map) )    
        objects = cmds.ls(sl=True, exactType='transform', l=True)
        if objects == None:
            raise IOError('No object selected')
            
        return self.w05_filterByMap(mapObj, map, objects)
        
     
    
    def w05_changeUI_cmd(self, *args):
        if w05_data != {} and cmds.checkBox( 'w05_06', q=True, v=True):
            threshold = cmds.floatSliderGrp( 'w05_02', q=True, v=True)
            minState = cmds.checkBox('w05_03', q=True, v=True)
            maxState = cmds.checkBox('w05_04', q=True, v=True)
            selObj = []
            if (minState ==True and maxState == True) or \
                (minState ==True and maxState == True):
                selectSomething = 1
                selObj.extend(w05_data.keys())
            elif minState == True and maxState == False:
                selObj = []
                for key, value in w05_data.iteritems():
                    if value < threshold:
                        selObj.append(key)            
            else:
                for key, value in w05_data.iteritems():
                    if value > threshold:
                        selObj.append(key)
            
            if selObj != []:
                cmds.select(selObj, r=True)
            else:
                cmds.select(cl=True)
               
    
    #w05_filterByMap('mapObjectShape', 'fractal1', cmds.ls(sl=True, type='transform', l=True) )
    
    def w05_filterByMap(self, mapObj, map, objects, *args):
        if isinstance( objects, str) or isinstance( objects, unicode):
            objects = [objects]
            
        if cmds.pluginInfo("nearestPointOnMesh",query=True,l=True)==False:
            cmds.loadPlugin("nearestPointOnMesh")
        
        uvNode = ''     
        for node in cmds.listConnections('%s.worldMesh'%(mapObj), s=False):
            if cmds.objectType(node) == 'nearestPointOnMesh' and cmds.listConnections(node+'.inPosition') == None:
                uvNode = node
                break
        if uvNode == '':
            uvNode = cmds.createNode("nearestPointOnMesh", n="mapUV")
            cmds.connectAttr(mapObj+'.worldMesh[0]', uvNode+'.inMesh',f=True)
        
        data = {}
        for object in objects:     
            objPos=cmds.objectCenter(object)
            cmds.setAttr(uvNode+'.inPosition', objPos[0], objPos[1], objPos[2], type="double3")
            atu = cmds.getAttr(uvNode+'.parameterU')
            atv = cmds.getAttr(uvNode+'.parameterV')
            
            
            rgb = cmds.colorAtPoint(map, o='RGB', u=atu, v=atv)
            value = mel.eval('rgb_to_hsv <<%s, %s, %s>>'%(rgb[0], rgb[1], rgb[2]) )[2]
            data[object]=(value)
        return data

#w05_selectByMapWin()