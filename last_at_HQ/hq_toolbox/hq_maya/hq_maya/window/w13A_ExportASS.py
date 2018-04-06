# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import os
from functools import partial


#------------w13A multi Export Ass
   
class w13A_ExportASS(object):
    
    _menuStr = '''{'path':'Rendering/Render/w13A_ExportASS()',
'icon':':/menuIconWindow.png',
'tip' : '批量导出ASS',
'html':True,
'usage':'$fun()',
}
'''
    def __init__(self):
        sceneName = cmds.file( q=True, sn=True, shn=True).rsplit('.',1)[0]
        wName = 'w13A_ExportASS'
        if cmds.window( wName, exists=True):
            cmds.deleteUI( wName )
        
        cmds.window( wName, title=wName, sizeable=False) 
        cmds.columnLayout('w13A_L00', p=wName, adj=True, rs=10)
        #cmds.button(l='Save Materials', p='w13A_L00', rs=True, h=50)
        
        #cmds.separator( p='w13A_L00', st="out")
        #--------------------------------------------------
        cmds.columnLayout( 'w13A_cl01', p='w13A_L00', adj=True)
        cmds.rowColumnLayout('w13A_cl01_01', p='w13A_cl01', nc=4, h=30, columnWidth=[(1, 30),(2,175), (3, 175)]  )
        cmds.intField('w13A_count', v=0, en=False, h=30)
        cmds.button(l='Rename Hairs', p='w13A_cl01_01', align='left', c=self.self.renameHair  )
        cmds.button(l='Assign aiHair shader', p='w13A_cl01_01', align='right', c='assignAiHairShader()', en=False)
        cmds.button(l='unspecified shaveHair', p='w13A_cl01_01', c=self.w13b_unspecefiedAiHair )
        cmds.separator(p='w13A_cl01', h=15, st='in')
        
        #--------------------------------------------------
        
        cmds.rowColumnLayout('w13A_cl01_02', p='w13A_L00', nc=6, columnWidth=[(1,40), (2, 140),(3, 90),(4,90),(5,90), (6,320)], rs=([1,10])  )
        index = 1
        self.w13A_addItem(index)
        
        #cmds.separator(p='w13A_L00', st='in')
        
        #cmds.checkBoxGrp( 'w13A_uiObjFilter', numberOfCheckBoxes=2, p='w13A_cl01', h=30, labelArray2=['nurbsCurve', 'Locator'], v1=True, v2=True )
        cmds.frameLayout('w13A_uiAssOptions', p='w13A_L00', label="ASS Export Options", collapsable=True,  borderStyle="in", collapse=True)
        #cmds.columnLayout( 'w13A_uiAssOptions', p='w13A_uiAss')#, cw=[(1,200),(2,80), (3,180),(4,150)] )
        
        cmds.checkBox( l='Use gzip Compression(.ass.gz)', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Export Bounding Box', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Use Binary Encoding', p='w13A_uiAssOptions', en=False, v=True)
        cmds.separator( p='w13A_uiAssOptions', st='in')
        cmds.checkBox( l='Options', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Cameras', p='w13A_uiAssOptions', en=False )
        cmds.checkBox( l='Lights', p='w13A_uiAssOptions', en=False )
        cmds.checkBox( l='Shapes', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Shaders', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Override Nodes', p='w13A_uiAssOptions', en=False, v=True)
        cmds.checkBox( l='Drivers', p='w13A_uiAssOptions',en=False )
        cmds.checkBox( l='Filters', p='w13A_uiAssOptions',en=False )
        
        #---------------------------------------------------
        cmds.rowColumnLayout('w13A_cl01_03', p='w13A_L00', nc=2)
        #cmds.checkBox('w13A_uiExportAll', l='All', p='w13A_cl01_03', h=30, cc='w13A_uiExportAll_cmd()')
        #cmds.button('w13A_uiExportMat', l='Export Materials', p='w13A_cl01_03', rs=True, c='w13A_uiExportMat_cmd()', en=False)
        cmds.button('self.w13A_uiExportAss', l='Export ASS Files', p='w13A_cl01_03', h=30,  c=self.w13A_uiExportAss )
        assDir = cmds.workspace(q =True, rootDirectory=True)+'data/'+sceneName+'/ass_hair'
        cmds.textFieldGrp('w13A_uiAssDirectory', p='w13A_cl01_03', l='Directory', h=30, cw2=(100,550), tx=assDir, ed=True)
        #cmds.button('w13A_uiShowExp', l='Open Directory', p='w13A_cl01_03', c='w13A_uiShowExp_cmd()', en=False )
        cmds.showWindow(wName)
    
    
    
    def renameHair(self, *args):        
        prefix = 'hairObj_'
        for sh in cmds.ls(exactType=['shaveHair','pfxHair', 'hairSystem'], l=True):
            papa = cmds.listRelatives( sh, parent=True, f=True)[0]
            papaNew = cmds.rename(papa, '%s#'%(prefix) )
            child = cmds.listRelatives( papaNew, type=['shaveHair','pfxHair', 'hairSystem'], shapes=True, f=True)[0]
            cmds.rename( child, '%sShape'%(papaNew) )
    
    
    def w13A_uiSetObj_cmd(self, index, *args):
        sceneName = cmds.file( q=True, sn=True, shn=True).rsplit('.',1)[0]  
        end = cmds.intField('w13A_count', q=True, v=True)
        oriSel = cmds.ls(sl=True, l=True)
        cmds.select(all=True, ado=True, r=True)
        rootObjs = cmds.ls(sl=True, type='transform', l=True)
        if oriSel==[]:
            cmds.select( cl=True )
        else:
            cmds.select( oriSel, r=True)
        
        
        sel = cmds.ls( sl=True, l=True)
        if sel==[]:
            return False
        uiObjs = []
        for i in range(1, end):
            tmp = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(i), q=True, tx=True)
            tmp = eval( tmp )
            uiObjs.extend( tmp )
            
        for obj in sel:
            if obj not in rootObjs or obj in uiObjs:
                return False
        
        oriObjs = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), q=True, tx=True)    
        if sel!=[]:
            hairs = cmds.listRelatives( cmds.ls( sl=True, l=True), ad=True, type=['shaveHair','pfxHair'], f=True)
            if hairs!=None:
                cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), e=True, tx=str(sel) )
                
                assName = sel[0] if len(sel)==1 else sel[0]+'_Objs'
                
                assName = sceneName + '_' + assName[1:]
                
                cmds.textFieldGrp('w13A_uiAssName%03d'%(index), e=True, en=True, tx=assName )
                
                cmds.checkBox('w13A_uiExport%03d'%(index), e=True, en=True, v=True)
                
        
        if end==index:        
            if cmds.objExists( oriObjs )==False and hairs:
                self.w13A_addItem(index+1)
        
        return True
    
    
    
    def w13A_addItem(self, index, *args):
        cmds.checkBox('w13A_uiExport%03d'%(index), l='%03d'%(index), p='w13A_cl01_02', bgc=(.4,.4,.4), en=False)
        cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), l='Root Grp', p='w13A_cl01_02', cw2=(45,90), en=False)
        cmds.button( l='Set Objects', p='w13A_cl01_02', c=partial(self.w13A_uiSetObj_cmd, index)  )
        cmds.button( l='Select Objects', p='w13A_cl01_02', c=partial(self.w13A_uiSelObj_cmd, index )  )
        cmds.button( l='Select Hair shave', p='w13A_cl01_02',  c=partial(self.w13A_uiSelHairs_cmd, index) )
        cmds.textFieldGrp('w13A_uiAssName%03d'%(index), l='ASS File', p='w13A_cl01_02', cw2=(40,260), en=False, cc=partial( self.w13A_uiPostfix_cmd, index)  )
        
        cmds.intField('w13A_count', e=True, v=index)
        
    
    def w13A_uiSelObj_cmd(self, index, *args):
        objs = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), q=True, tx=True)
        if objs!='':
            objs = eval(objs)
            for obj in objs:            
                if cmds.objExists( obj )==False:
                    raise IOError( '%s is not exist!'%(obj) )
            else:
                cmds.select( objs, r=True )
                
    def w13A_uiSelHairs_cmd(self, index, *args):
        objs = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), q=True, tx=True)
        if objs!='':
            objs = eval(objs)
            hairs = cmds.listRelatives( objs, ad=True, type=['shaveHair','pfxHair'], f=True)
            hairs = cmds.listRelatives( hairs, parent=True, f=True)
            if hairs:
                cmds.select( hairs, r=True)
            else:
                raise IOError( 'No has shaveHair or pfxHair of %s children'%( str(objs) ) )
                
    def w13A_uiExportAss(self, *args):
        end = cmds.intField('w13A_count', q=True, v=True)
        exportDir = cmds.textFieldGrp('w13A_uiAssDirectory', q=True, tx=True) #cmds.workspace(q =True, rootDirectory=True)
        exportDir = exportDir.replace('\\', '/')
        if os.path.exists( exportDir )==False:
            try:
                os.makedirs( exportDir )
            except:
                sceneName = cmds.file( q=True, sn=True, shn=True).rsplit('.',1)[0]
                assDir = os.path.join( cmds.workspace(q =True, rootDirectory=True), 'data', sceneName, 'ass_hair')
                assDir = assDir.replace('\\', '/')
                cmds.textFieldGrp('w13A_uiAssDirectory', e=True, tx=assDir)
                exportDir = assDir
                
    
        startF = cmds.playbackOptions( q=True, min=True)
        endF = cmds.playbackOptions( q=True, max=True)
        assInfoStr = ''
        for index in range(1, end):
            objs = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), q=True, tx=True)
            expable = cmds.checkBox('w13A_uiExport%03d'%(index), q=True, v=True)
            assInfoStr +='\n'+str()
            assInfoFile = open(os.path.join(exportDir, 'ass_hairInfo.txt'), 'w')
    
      
        import datetime
        curTime = datetime.datetime.now().date().timetuple()    
        today =  int( "%d%02d%02d"%(curTime[0],curTime[1],curTime[2]) )
        
        infoFileName = os.path.join(exportDir, 'ass_hairInfo.txt')
        infoFile = open(infoFileName, 'a')
        sceneName = cmds.file( q=True, sn=True, shn=True).rsplit('.',1)[0]
        infoStr = '\n\n%s%s\n%s'%(sceneName, '*'*50, today)
        infoFile.write( infoStr  )
        infoFile.close()
        
        for index in range(1, end):
            objs = cmds.textFieldGrp('w13A_uiRootGrp%03d'%(index), q=True, tx=True)
            expable = cmds.checkBox('w13A_uiExport%03d'%(index), q=True, v=True)
            
            
            if objs!='' and expable:
                assFile = cmds.textFieldGrp('w13A_uiAssName%03d'%(index), q=True, tx=True)            
                assFilePath = '%s/%s/%s.ass'%(exportDir, assFile, assFile)
                objs = eval(objs)
                hairs = cmds.listRelatives( objs, ad=True, type=['shaveHair','pfxHair'], f=True)
                hairs = cmds.listRelatives( hairs, parent=True, f=True)
                cmds.select(hairs, r=True)
                try:
                    cmds.arnoldExportAss(f=assFilePath, s=True, startFrame=startF, endFrame=endF, mask=57, lightLinks=False, frameStep=1.0, compressed=True, boundingBox=True, shadowLinks=False,cam='perspShape')
                    infoFile = open( infoFileName, 'a')
                    infoStr = '\n\n' + assFile + '\n' +str(objs)
                    infoFile.write( infoStr )
                    infoFile.close()                
                except:
                    pass
                
    def w13b_unspecefiedAiHair(self, *args):  
        windowName = 'w13b_unspecefiedAiHair'        
        if cmds.window( windowName, title='shaveHair and hair', exists=True):
            cmds.deleteUI( windowName)
        sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0] 
        cmds.window(windowName, title=windowName, sizeable=True)
        cmds.formLayout("w13b_layout", p=windowName)    
        cmds.textScrollList( 'w13b_hair', p="w13b_layout", allowMultiSelection=True, en=0, bgc=[0,0,0], showIndexedItem=4, doubleClickCommand='self.w13b_doubleClick_cmd()')
        cmds.formLayout( 'w13b_layout', edit=True, attachForm=[('w13b_hair', 'top', 5), ('w13b_hair', 'bottom', 5), ('w13b_hair', 'left', 5),('w13b_hair', 'right', 5)] )    
        cmds.showWindow( windowName )
        
        #hairs = cmds.ls( exactType=['shaveHair','hairSystem'], l=True)
        forAssign = []
        for hair in cmds.ls( exactType='shaveHair'):
            if cmds.listConnections(hair+'.aiHairShader')==None:
                forAssign.append( hair )
    
        for hair in cmds.ls( exactType='hairSystem' ):
            if cmds.listConnections(hair+'.aiHairShader')==None and cmds.listConnections( hair+'.outputRenderHairs'):
                forAssign.append( hair)
        
        cmds.textScrollList('w13b_hair', e=True, en=True, removeAll=True)
        for hairNode in forAssign:
            cmds.textScrollList('w13b_hair', e=True, append=hairNode)    
        
    
    def w13b_doubleClick_cmd(self, *args):
        item = cmds.textScrollList( 'w13b_hair', q=True, selectItem=True)
        cmds.select( item, r=True)
        
    #------------w13A End