#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:jingxiaochuan
#--date--:2017-06-14
import maya.cmds as cmds
def check_feetMask():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查脚底板是否加入NoRender组'}
    '''
    NRdisLayers = cmds.ls('NoRender', type='displayLayer')
    wrongs =[]
    if NRdisLayers!=[]:
        for NRdisLayer in NRdisLayers:
            meshcol =  cmds.listConnections(sel+".drawInfo",s=0)
            feetMaskgrps = cmds.ls("*_feetMask_g")
            for feetMaskgrp in feetMaskgrps:
                if feetMaskgrp not in meshcol:
                    feetMaskmesh = cmds.listRelatives(feetMaskgrp,ad=1,type="mesh")
                    feetMasktr = [cmds.listRelatives(f,p=1)[0] for  f in feetMaskmesh]
                    if meshcol!=None or feetMasktr!=None:
                        adj = list(set(feetMask).intersection(set(meshcol)))
                        if len(adj)==4:
                            pass
                        else:
                            wrong = [w for w in feetMasktr if w not in adj]
                            wrongs += wrong
                else:
                    pass
    else:
        wrongs.append("no NoRenderLayer!!")
    return wrongs