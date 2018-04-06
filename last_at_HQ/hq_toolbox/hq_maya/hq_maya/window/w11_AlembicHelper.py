# -*- coding: utf-8 -*-
import maya.cmds as cmds
from functools import partial

import qsMaya as qm 
import window as qmw

class w11_AlembicHelper(object):
    _menuStr = '''{'del_path':'Pipeline Cache/w11_AlembicHelper()',
'icon':'$ICONDIR/alembic.png',
'tip' : '导出导入abc',
'usage':'$fun()',
}
'''
    
    def __init__(self):
        self.__colors = [(.3, .8, .3), (.8, .3, .3)]
        wName = 'w11_AlembicHelper'
        if cmds.window(wName, exists=True):
            cmds.deleteUI( wName )        
        
        cmds.window( wName, title=wName, sizeable=False)
        
        mainLayout = cmds.formLayout( p=wName )
        
        #----------Get CoudGrp UI
        firstFrame = cmds.frameLayout( p=mainLayout, label="Export", marginHeight=5, marginWidth=5, w=320, bgc=(0.15,0.15,0.3), collapsable=False, cl=False, borderStyle="in")
        firstCol = cmds.rowColumnLayout( p=firstFrame, numberOfColumns=2, columnWidth=[(1, 180), (2, 100)], cs=[(1,5),(2,10)], rs=(1,15) )
        self.__importReference_text = cmds.text( p=firstCol, l=unicode('导入所有reference'), al='right', wordWrap=True)
        cmds.separator( )
        #cmds.button( p=firstCol, l=unicode('导入参考'), h=40, c=self.importReference )
        
        
        self.__createMat_text = cmds.text( p=firstCol, l=unicode('选择要导出的物体，创建matInfo属性保存材质\nalembic_output_createMatAttr()'), al='right', wordWrap=True )
        cmds.button(p=firstCol, l=unicode('创建材质'), h=40, c=self.createMatInfo )
        
        self.__createHairShave_txt = cmds.text(p=firstCol, l=unicode('创建hair曲线和hairData、shaveObjId属性\nalembic_output_hairAndShave()'), al='right', wordWrap=True)
        cmds.button(p=firstCol, l=unicode('创建属性'), h=40, c=self.createHairAndShave )
        
        self.__intermediateObj_text = cmds.text( p=firstCol, l=unicode('隐藏物体，优化导出\nw20_intermediateObjects()'), al='right', wordWrap=True )
        cmds.button(p=firstCol, l=unicode('隐藏物体'), al='right', h=40, c=self.intermediateObjects )
        
        self.__exportAbc_text = cmds.text(p=firstCol, l=unicode('导出abc'), al='right', wordWrap=True )
        cmds.separator( )
        #cmds.button(p=firstCol, l=unicode('导出abc'), h=40, c=self.exportAbc )
        
        self.__grpShaveObjs_text = cmds.text(p=firstCol, l=unicode('创建shaveObjsGrp,shaveHairGrps两个组\nalembic_output_groupShaveObjs()'), al='right', wordWrap=True)
        cmds.button(p=firstCol, l=unicode('打组shave节点'), h=40, c=self.grpShaveObjs )
        
        
        self.__exportToMayafile_text = cmds.text(p=firstCol, l=unicode('导出locator,打包的shave节点和materials'), al='right', wordWrap=True )
        cmds.button(p=firstCol, l=unicode('导出'), h=40, rs=False, c=self.exportToMayafile  )
        
        
        
        secFrame = cmds.frameLayout( p=mainLayout, label="Import", marginHeight=5, marginWidth=5, w=320, bgc=(0.15,0.15,0.3), collapsable=False, cl=False, borderStyle="in")
        secCol = cmds.rowColumnLayout( p=secFrame, numberOfColumns=2, columnWidth=[(1, 180), (2, 100)], cs=[(1,5),(2,10)], rs=(1,15) )
        
        cmds.text(l=unicode('打开导出的材质文件'), al='right')
        cmds.separator( )
        
        
        cmds.text(l=unicode('导入abc'), al='right')
        cmds.separator()
        #cmds.button(l=unicode('导入abc'), h=40)
        
        
        self.__assignMat_text = cmds.text( l=unicode('用matInfo属性恢复材质\nalembic_import_assignMaterialsFromAttr'), al='right', wordWrap=True  )
        cmds.button(l=unicode('恢复材质'), h=40, c=self.assignMat )
        
        self.__recreateHairAndShave_text = cmds.text( l=unicode('恢复hair和shave'), al='right', wordWrap=True   )
        cmds.button(l=unicode('恢复hair和shave'), h=40, c=self.recreateHairAndShave )
        
        
        thirdFrame = cmds.frameLayout( p=mainLayout, label=unicode("说明"), marginHeight=5, marginWidth=5, bgc=(0.15,0.15,0.3), collapsable=False, cl=False, borderStyle="in")
        thirdColumnLayout = cmds.columnLayout( p=thirdFrame, columnAttach=('both', 5), adj=True )
        cmds.text( p=thirdColumnLayout, align='left', font='boldLabelFont', l=unicode("        这些导出操作会当前的maya文件做很多处理，特别是长shave毛发的物体，导出前，先做好当前的文件的备份;"), wordWrap=True, rs=False)
        
        
        cmds.formLayout(mainLayout, edit=True,
                        attachForm=[(firstFrame, "top", 3),    (firstFrame, "left", 3), (firstFrame, 'bottom', 3),
                                    #('uiLayoutFL',  "top", 1),    ('uiLayoutFL',  'left', 3),
                                    (secFrame, "top", 3),    (secFrame, "right", 3),
                                    (thirdFrame, 'bottom', 3), (thirdFrame, 'right', 3)
                                    ],
                        attachControl = [(secFrame, 'left', 5, firstFrame),
                                         (thirdFrame, 'top', 3, secFrame), (thirdFrame, 'left', 5, firstFrame)
                                         ]
                        )        
        
        cmds.showWindow(wName)
    
        
    
    def createMatInfo(self, *args):
        try:
            qm.alembic_output_createMatAttr()
        except:
            cmds.text(self.__createMat_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__createMat_text, e=True, bgc=self.__colors[0] )
    
    def createHairAndShave(self, *args):
        try:
            qm.alembic_output_hairAndShave()
        except:
            cmds.text(self.__createHairShave_txt, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__createHairShave_txt, e=True, bgc=self.__colors[0] )
        
    def intermediateObjects(self, *args):
        try:
            qmw.w20_intermediateObjects( )
        except:
            cmds.text(self.__intermediateObj_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__intermediateObj_text, e=True, bgc=self.__colors[0] )
        
    
    def exportAbc(self, *args):
        try:
            exportabc()
        except:
            cmds.text(self.__exportAbc_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__exportAbc_text, e=True, bgc=self.__colors[0] )
        
    def grpShaveObjs(self, *args):
        try:
            qm.groupShaveObjs()
        except:
            cmds.text(self.__grpShaveObjs_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__grpShaveObjs_text, e=True, bgc=self.__colors[0] )
        
    def exportToMayafile(self,*args):
        try:
            qm.exportAllMaterials()
        except:
            cmds.text(self.__exportToMayafile_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__exportToMayafile_text, e=True, bgc=self.__colors[0] )
        
    
    
    def assignMat(self,*args):
        try:
            qm.qm.alembic_import_assignMaterialsFromAttr( )
        except:
            cmds.text(self.__assignMat_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__assignMat_text, e=True, bgc=self.__colors[0] )
    
    
    def recreateHairAndShave(self,*args):
        try:
            qm.alembic_import_hairAndShave( )
        except:
            cmds.text(self.__recreateHairAndShave_text, e=True, bgc=self.__colors[1] )
            return
        cmds.text(self.__recreateHairAndShave_text, e=True, bgc=self.__colors[0] )