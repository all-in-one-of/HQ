#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:lingyc
#--date--:2017-06-09
import maya.cmds as cmds
def check_aiSubdiv():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查Arnold渲染细分大于3的物体'}
    '''
    all_polymesh= cmds.ls(typ= 'mesh')
    aiSubdiv_soBig= []
    for i in range(len(all_polymesh)):
        try:        
            aiSubdiv_type= cmds.getAttr(all_polymesh[i]+'.aiSubdivType')#arnold细分类型
            aiSubdiv_iterations= cmds.getAttr(all_polymesh[i]+'.aiSubdivIterations')#arnold细分参数
            if aiSubdiv_type != 0 and aiSubdiv_iterations> 3:
                aiSubdiv_soBig.append(all_polymesh[i])
        except:
            pass
    return aiSubdiv_soBig