#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:huwenbin
#--date--:2017-06-13
import maya.cmds as cmds
def check_render_Options():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查Options设置是否正确'}
    '''
    render_Options=["defaultRenderGlobals.preMel","defaultRenderGlobals.poam","defaultRenderGlobals.prlm","defaultRenderGlobals.polm","defaultRenderGlobals.preRenderMel","defaultRenderGlobals.pom"]    
    other_render_Options=[]
    for i in range(len(render_Options)):
        render_Options_name=cmds.getAttr(render_Options[i])
        if render_Options_name!=None:
            other_render_Options.append(render_Options[i])
    return other_render_Options