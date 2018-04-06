# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds



class w12A_hideHairs(object):
    _menuStr = '''{'del_path':'Dynamics/nHair/w12A_hideHairs()',
'icon':':/hairSystem.svg',
'html':True,
'usage':'$fun()',
}
'''
    def __init__(self):
        wName = 'w12A_HideHairs'
        if cmds.window( wName, exists=True):
            cmds.deleteUI( wName )
        
        cmds.window( wName, title=wName, sizeable=True) 
        
        cmds.formLayout('w12A_uiMainLay',p=wName)
        cmds.frameLayout('w12A_uiUtilLay', p="w12A_uiMainLay", label="Utility", collapsable=True,  borderStyle="in")
        cmds.rowColumnLayout( 'w12A_uiRowLay_02', p='w12A_uiUtilLay', nc=2)#, cw=[(1,200),(2,80), (3,180),(4,150)] )
        
        cmds.button( l='Rename Hairs', p='w12A_uiRowLay_02', h=30, c=self.renameHair )
        cmds.button( l='Assign aiHair shader', p='w12A_uiRowLay_02',h=30, c=self.assignAiHairShader )
        cmds.separator( p='w12A_uiRowLay_02', st="out",  h=10)
        cmds.separator( p='w12A_uiRowLay_02', st="out",  h=10)
        
        cmds.optionMenu( 'w12A_uiCameras', l='Cameras:', p='w12A_uiRowLay_02', h=30, w=200)
        for cam in cmds.listRelatives( cmds.ls( cameras=True), parent=True, f=True):
            cmds.menuItem( label=cam, p= 'w12A_uiCameras')
        cmds.button('w12_uiUpdataCam',  l='Update cam', p='w12A_uiRowLay_02', w=80, c=self.w12A_uiUpdateCam_cmd )
        cmds.separator( p='w12A_uiRowLay_02', st="in",  h=10)
        cmds.separator( p='w12A_uiRowLay_02', st="in",  h=10)
        cmds.intSliderGrp( 'w12A_uiStep', p='w12A_uiRowLay_02', field=True, label='Key step', cw3=[50,30,100], h=30, minValue=1, maxValue=100, fieldMinValue=1, fieldMaxValue=100, value=1)
        cmds.button( 'w12A_uiDisToCamera', l='Get distance to camera',  p='w12A_uiRowLay_02', h=30, c=self.w12A_uiAddDistAttr )
        #cmds.button( 'w12A_uiListAll', l='Sort by minimum distance',  p='w12A_uiRowLay_02')
        
        
        
        
        cmds.rowColumnLayout( 'w12A_uiRowLay_top', p='w12A_uiMainLay', nc=10, cs=[(4,10),(6,10)], cw=[(1,28),(2,150),(3,50),(4,150),(5,50),(6,40)  ]  ) 
        cmds.text('w12A_uiCount', l=0, p='w12A_uiRowLay_top')
        cmds.button(l='Get Selected', p='w12A_uiRowLay_top', h=30, c=self.w12A_GetAll_cmd )
        cmds.button('w12A_uiSelAllFurs', l='Sel All', p='w12A_uiRowLay_top', c=self.w12A_uiSelAllFurs_cmd )
        cmds.button('w12A_uiSortByDist', l='Sort by minimum distance', p='w12A_uiRowLay_top', en=False, c=self.w12A_uiSortByDist_cmd  )
        #cmds.text( p='w12A_uiRowLay_top', en=False)
        cmds.button('w12A_uiSelAllSurs', l='Sel All', p='w12A_uiRowLay_top', c=self.w12A_uiSelAllSurs_cmd   )
        #cmds.text(l='Select', p='w12A_uiRowLay_top' )
        #cmds.button(l='', p='w12A_uiRowLay_top')
        #cmds.button(l='', p='w12A_uiRowLay_top')
        #cmds.button(l='', p='w12A_uiRowLay_top')
        #cmds.radioButtonGrp( 'w12A_uiSelChoose', numberOfRadioButtons=2, cw2=(40,400), labelArray2=('Hair', 'Surface' ), sl=1 )
        
        ###
        cmds.scrollLayout('w12A_uiScroLay', p='w12A_uiMainLay', cr=True)
        ####
        
        cmds.rowColumnLayout( 'w12A_uiRowLay', p='w12A_uiScroLay', nc=5,  cs=[(4,10)], cw=[(1,25),(2,150),(3,50),(4,150),(5,50)])
        
            
                
        cmds.formLayout('w12A_uiMainLay', e=True,\
                        attachForm=[('w12A_uiUtilLay', 'top', 3),('w12A_uiUtilLay', 'left', 3),('w12A_uiUtilLay', 'right', 3),\
                                    ('w12A_uiRowLay_top', 'left', 3),('w12A_uiRowLay_top', 'right', 3),\
                                    ('w12A_uiScroLay', 'bottom', 3),('w12A_uiScroLay', 'left', 3),('w12A_uiScroLay', 'right', 3)
                                    ],\
                        attachControl=[('w12A_uiRowLay_top', 'top', 4, 'w12A_uiUtilLay'),\
                                        ('w12A_uiScroLay', 'top', 4, 'w12A_uiRowLay_top')\
                                        ]\
                        )                
        
        cmds.showWindow(wName)
    
    
    def w12A_uiUpdateCam_cmd(self, *args):
        items = cmds.optionMenu( 'w12A_uiCameras', q=True, itemListLong=True)
        if items:
            cmds.deleteUI( items )
        for cam in cmds.listRelatives( cmds.ls( cameras=True), parent=True, f=True):
            cmds.menuItem( label=cam, p= 'w12A_uiCameras')
            
    
    
    
    def w12A_uiMarker_cmd(self, i, *args):
        bgcId = cmds.radioButtonGrp( 'w12A_uiMarker%03d'%(i), q=True, sl=True) -1
        bc = ([0.26666666666666666, 0.26666666666666666, 0.26666666666666666], [1,0,0], [0,1,0])[bgcId]
        cmds.textField( 'w12A_uiShave%03d'%(i),  e=True, bgc=bc  )
        cmds.textField( 'w12A_uiSur%03d'%(i),   e=True, bgc=bc  )
    
    
    
    def w12A_uiAddDistAttr(self, *args):
        #objs = []
        shaveHairs = self.getShaveHairData() 
        hairs = {}   
        for hair in shaveHairs:
            temp = hair[0][0] if str( type(hair[0]) )=="<type 'tuple'>" else hair[0]
            hairs[temp] = hair
        for pfx in cmds.ls(exactType='pfxHair'):
            hairs[pfx]=pfx
            #objs.extend(  )
        
        objs = hairs.keys()
        #QM.delAttr(  hairs.values(), ['distCam'] )
        delAttr(  objs, ['distCam'] )
        cmds.addAttr( objs, ln='distCam', at='float')
        startFrame = int( cmds.playbackOptions( q=True, min=True) )
        endFrame = int( cmds.playbackOptions( q=True, max=True)+1 )
        step = cmds.intSliderGrp( 'w12A_uiStep', q=True, v=True)
        
        
        
        cam = cmds.optionMenu( 'w12A_uiCameras', q=True, v=True)
        for f in range(startFrame, endFrame, step):
            cmds.currentTime( f, e=True)
            camCenter = cmds.objectCenter( cam )  
            for obj in objs:
                objCenter = cmds.objectCenter( obj )
                dist = newOM.MPoint( camCenter ).distanceTo( newOM.MPoint(objCenter) )            
                cmds.setKeyframe(obj+'.distCam',  v=dist)
    
    def w12A_uiSortByDist_cmd(self, *args):
        pass
    
    
    def getShaveHairData(self, *args):
        shaveHairs = []
        notGet = []
        for hair in cmds.ls( exactType='shaveHair', l=True):
            meshs = cmds.listConnections( hair+'.inputMesh', d=False)
            surfaces = cmds.listConnections( hair+'.inputSurface', d=False)
            curves = cmds.listConnections( hair+'.inputCurve', d=False)
            hairPapa = cmds.listRelatives( hair, parent=True, f=True)[0]
            if meshs!=None:
                for mesh in meshs:
                    shaveHairs.append( (mesh,hairPapa) )
            
                
            if surfaces!=None:
                for sur in surfaces:
                    shaveHairs.append( (sur,hairPapa) )
            
            if curves!=None:
                if len(curves)<3:
                    shaveHairs.append( (curves[0],hairPapa) )
                else:
                    temp = set()
                    for cur in curves:
                        history = cmds.listHistory( cur, lv=6)                
                        for node in history:
                            #print node
                            if cmds.objectType( node ) in ('mesh','nurbsSurface'):
                                temp.add( node )
                                break
                    temp = tuple(temp)[0] if len( temp )==1 else tuple( temp )
                    shaveHairs.append( (temp, hairPapa) )
        return shaveHairs
    
    
    
    def w12A_GetAll_cmd(self, all=False, *args):
        layChildren = cmds.rowColumnLayout( 'w12A_uiRowLay', q=True, childArray=True)
        if layChildren:
            cmds.deleteUI( layChildren )
            cmds.text('w12A_uiCount', e=True, l=0)
            
        shaveHairs = []
        notGet = []
        if all:
            hairs = cmds.ls( exactType='shaveHair', l=True)
            pfxHair = cmds.ls(exactType='pfxHair')
        else:
            hairs = cmds.listRelatives( cmds.ls( sl=True, l=True), ad=True, type='shaveHair', f=True)
            hairs = [] if hairs==None else hairs
            pfxHair = cmds.listRelatives( cmds.ls( sl=True, l=True), ad=True, type='pfxHair', f=True)
            pfxHair = [] if pfxHair==None else pfxHair
            
            
            
        for hair in hairs:
            meshs = cmds.listConnections( hair+'.inputMesh', d=False)
            surfaces = cmds.listConnections( hair+'.inputSurface', d=False)
            curves = cmds.listConnections( hair+'.inputCurve', d=False)
            hairPapa = cmds.listRelatives( hair, parent=True, f=True)[0]
            if meshs!=None:
                for mesh in meshs:
                    shaveHairs.append( (mesh,hairPapa) )
            
                
            if surfaces!=None:
                for sur in surfaces:
                    shaveHairs.append( (sur,hairPapa) )
            
            if curves!=None:
                if len(curves)<3:
                    shaveHairs.append( (curves[0],hairPapa) )
                else:
                    temp = set()
                    for cur in curves:
                        history = cmds.listHistory( cur, lv=6)                
                        for node in history:
                            #print node
                            if cmds.objectType( node ) in ('mesh','nurbsSurface'):
                                temp.add( node )
                                break
                    temp = tuple(temp)[0] if len( temp )==1 else tuple( temp )
                    shaveHairs.append( (temp, hairPapa) )
                    
                    #notGet.append( hair )
                    #polyEdge = cmds.listConnections( curves[0]+'.create', d=False, type='polyEdgeToCurve')
                    #if polyEdge!=None:
                        #mesh = cmds.listConnections( polyEdge[0]+'.inputPolymesh')
                        #if mesh!=None:
                            #shaveHairs.append( (mesh[0], hairPapa) )
             
        
        count = cmds.text('w12A_uiCount', q=True, l=True)
        index = int(count)
        for obj, shave in shaveHairs:
            index+=1        
            bc = ([0.26666666666666666, 0.26666666666666666, 0.26666666666666666], [.3,.3,.3])[index%2]
            cmds.text( l='%03d'%(index), p='w12A_uiRowLay', bgc=bc)
            cmds.textField( 'w12A_uiShave%03d'%(index),     p='w12A_uiRowLay', tx=shave, ed=False, bgc=bc)
            cmds.button(    'w12A_uiSelShave%03d'%(index), l='Sel', p='w12A_uiRowLay', bgc=bc, c='self.w12A_uiSelFurNode_cmd(%d)'%(index) )
            
            cmds.textField( 'w12A_uiSur%03d'%(index),        p='w12A_uiRowLay', bgc=bc, tx=str(obj), ed=False)
            cmds.button(    'w12A_uiSelSur%03d'%(index),  l='Sel', p='w12A_uiRowLay', bgc=bc, c='self.w12A_uiSelFurSkin_cmd(%d)'%(index) )
            
            #cmds.radioButtonGrp( 'w12A_uiMarker%03d'%(index), p='w12A_uiRowLay', numberOfRadioButtons=3, label='Marker',  cw4=(40,20,20,20), sl=1, vis=False, cc='self.w12A_uiMarker_cmd(%d)'%(index) )
            #cmds.button(    'w12A_uiSetWrap%03d'%(index),    l='Set', p='w12A_uiRowLay', c='w12A_uiSetWrap_cmd(%d)'%(index) )
            #cmds.button(    'w12A_uiDoWrap%03d'%(index), l='Wrap', p='w12A_uiRowLay')  #, c='w12A_uiDoWrap_cmd(%d)'%(index) )
        cmds.text('w12A_uiCount', e=True, l=index)
        # Result: u'w12A_uiCount' # 
        if notGet!=[]:
            pfxHair.extend( notGet )
        print ':::', notGet, pfxHair
        if notGet!=[] or pfxHair!=[]:
            for pfx in notGet+pfxHair:
                index+=1
                bc = ([0.25, 0.25, 0.25], [.35,.35,.35])[index%2]
                pfxPapa = cmds.listRelatives( pfx, parent=True, f=True)[0]
                
                cmds.text( l='%03d'%(index), p='w12A_uiRowLay', bgc=bc)
                cmds.textField( 'w12A_uiShave%03d'%(index),     p='w12A_uiRowLay', bgc=bc, tx=pfxPapa, ed=False)
                cmds.button(    'w12A_uiSelShave%03d'%(index), l='Sel', p='w12A_uiRowLay', bgc=bc, c='self.w12A_uiSelFurNode_cmd(%d)'%(index) )
                
                cmds.textField( 'w12A_uiSur%03d'%(index),  p='w12A_uiRowLay', tx=pfxPapa,  ed=False, bgc=bc)
                cmds.button(    'w12A_uiSelSur%03d'%(index),  l='Sel', p='w12A_uiRowLay', en=False, bgc=bc)
                
                
                #cmds.radioButtonGrp( 'w12A_uiMarker%03d'%(index), p='w12A_uiRowLay', numberOfRadioButtons=3, label='Marker',  cw4=(40,20,20,20), sl=1, vis=False, cc='self.w12A_uiMarker_cmd(%d)'%(index) )
                #cmds.textField( 'w12A_uiWrap%03d'%(index),    p='w12A_uiRowLay', ed=False)
                #cmds.button(    'w12A_uiSetWrap%03d'%(index),    l='Set', p='w12A_uiRowLay', en=False)
                #cmds.button(    'w12A_uiDoWrap%03d'%(index), l='Wrap', p='w12A_uiRowLay', en=False)    
                cmds.text('w12A_uiCount', e=True, l=index)
    
           
    def w12A_uiSelAllFurs_cmd(self, *args):
        count = int( cmds.text('w12A_uiCount', q=True, l=True) )+1
        shaves = []
        for i in range( 1,count ):
            shaves.append( cmds.textField( 'w12A_uiShave%03d'%(i),  q=True, tx=True) )
        if shaves!=[]:
            cmds.select( shaves, r=True)
          
    
    def w12A_uiSelAllSurs_cmd(self, *args):
        count = int( cmds.text('w12A_uiCount', q=True, l=True) )+1
        surs = []
        for i in range( 1,count ):
            sur = cmds.textField( 'w12A_uiSur%03d'%(i),  q=True, tx=True)
            if sur[0]=='(' and sur[-1]==')':
                sur = eval( sur )
                surs.append( sur[0] )
            else:
                surs.append( sur  )
        if surs!=[]:
            cmds.select( surs, r=True)
            
    def w12A_uiSelFurNode_cmd(self, index, *args):
        shaveNode = cmds.textField( 'w12A_uiShave%03d'%(index),   q=True, tx=True)
        cmds.select(shaveNode, r=True )
    
         
    def w12A_uiSelFurSkin_cmd(self, index, *args):
        sur = cmds.textField( 'w12A_uiSur%03d'%(index),   q=True, tx=True)
        if sur[0]=='(' and sur[-1]==')':
            sur = eval(sur)
        cmds.select(sur, r=True )
    
    
    #def w12A_uiSelByColor():
    #    colorId = 0
    #    uiName = ('w12A_uiShave','w12A_uiSur')[0]
    #    surUI = 
    #    forSel = []
    #    count = int( cmds.text('w12A_uiCount', q=True, l=True) )+1
    #    surs = []
    #    for i in range( 1,count ):
    #        obj = cmds.textField( '%s%03d'%(uiName,i), q=True, tx=True)
        
                    
    
    def renameHair(self, *args):        
        prefix = 'hairObj_'
        for sh in cmds.ls(exactType=['shaveHair','pfxHair'], l=True):    
            papa = cmds.listRelatives( sh, parent=True, f=True)[0]
            papaNew = cmds.rename(papa, '%s#'%(prefix) )
            child = cmds.listRelatives( papaNew, type=['shaveHair','pfxHair'], shapes=True, f=True)[0]
            cmds.rename( child, '%sShape'%(papaNew) )
    
    def assignAiHairShader( self, *args ):
        hairs = cmds.ls( exactType=['shaveHair','hairSystem'], l=True)
        forAssign = []
        for hair in hairs:
            if cmds.listConnections(hair+'.aiHairShader')==None:
                forAssign.append( hair )
        if forAssign!=[]: 
            #existAiHair = cmds.ls(exactType='aiHair')
            #if existAiHair==None:    
            aiHair = cmds.createNode( 'aiHair')
            #else:
                #aiHair = existAiHair[0]
            for hair in forAssign:
                cmds.setAttr( hair+'.aiOverrideHair', True)
                try:
                    cmds.connectAttr(aiHair+'.outColor', hair+'.aiHairShader', f=True)
                except:
                    pass
           
    def lostMaterials():
        surfaces = cmds.ls( exactType=['mesh', 'nurbsSurface'], noIntermediate=True )
        lostMat = []
        for sur in surfaces:
            if cmds.listConnections( sur, type='shadingEngine', s=False)==None:
                lostMat.append( sur )
        if lostMat==[]:
            return None
        else:
            cmds.select( lostMat, r=True)
            return lostMat
