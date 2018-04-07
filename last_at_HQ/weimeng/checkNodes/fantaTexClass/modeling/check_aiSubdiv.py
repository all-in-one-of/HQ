#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:lingyc
#--date--:2017-06-09
import maya.cmds as cmds
def check_aiSubdiv():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'���Arnold��Ⱦϸ�ִ���3������'}
    '''
    all_polymesh= cmds.ls(typ= 'mesh')
    aiSubdiv_soBig= []
    for i in range(len(all_polymesh)):
        try:        
            aiSubdiv_type= cmds.getAttr(all_polymesh[i]+'.aiSubdivType')#arnoldϸ������
            aiSubdiv_iterations= cmds.getAttr(all_polymesh[i]+'.aiSubdivIterations')#arnoldϸ�ֲ���
            if aiSubdiv_type != 0 and aiSubdiv_iterations> 3:
                aiSubdiv_soBig.append(all_polymesh[i])
        except:
            pass
    return aiSubdiv_soBig