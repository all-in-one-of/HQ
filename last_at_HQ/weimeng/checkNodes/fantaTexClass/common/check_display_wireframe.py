#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:libin
#--date--:2017-06-13
import maya.cmds as cmds
def check_display_wireframe():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查提交文件的视窗是否为线框模式'}
    '''
    nowireframe =[]
    modelPanels_all = cmds.getPanel(type="modelPanel")
    for currentPanel in modelPanels_all:
        displaytype = cmds.modelEditor(currentPanel,displayAppearance=1,q=1)
        zongshu = len(modelPanels_all)
        if displaytype!="wireframe":
            nowireframe.append(currentPanel)
    return nowireframe
if __name__=='__main__':
    adj = check_display_wireframe()
    if adj ==[]:
        print "-------视图为线框显示-------\n",
    else:
        print "-------视图为非线框显示-------\n",