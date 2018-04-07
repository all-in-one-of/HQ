#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:lingyc
#--date--:2017-06-09
import maya.cmds as cmds
def check_renderLayer():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'ºÏ≤È∂‡”‡‰÷»æ≤„'}
    '''
    allRenderLayer= set(cmds.ls(typ= 'renderLayer'))
    normalRendeLayer= {'defaultRenderLayer'}
    otherRenderLayer= list(allRenderLayer.difference(normalRendeLayer))
    return otherRenderLayer