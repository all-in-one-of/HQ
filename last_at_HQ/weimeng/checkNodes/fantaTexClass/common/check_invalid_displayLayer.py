#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:huwenbin
#--date--:2017-06-13
import maya.cmds as cmds
def check_invalid_displayLayer():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查多余显示层'}
    '''
    all_layer=set(cmds.ls(typ="displayLayer"))
    remove_layer={"defaultLayer","ori_sim","NoRender","TX"}
    delete_layer=list(all_layer.difference(remove_layer))
    return delete_layer