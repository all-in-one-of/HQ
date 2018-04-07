#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:yujing
#--date--:2017-06-14
import maya.cmds as cmds
def check_catchName():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查动捕提交文件名字规范'}
    '''
    namelists = ["catch_all|*_geo","catch_all|character_joint"]
    namelistInValid = []
    if cmds.objExists("catch_all")==True:
        wholemesh =[w for w in cmds.listRelatives('catch_all',ad=1,type="mesh")]
        wholemeshtr = [cmds.listRelatives(s,p=1,type="transform")[0] for s in wholemesh ]
        wholemeshs = wholemesh+wholemeshtr
        geolist = cmds.ls('*_geo*')
        wrongmesh = [b for b in  list(set(wholemeshs)) if b not in geolist]
        namelistInValid  += wrongmesh
        for namelist in namelists:
            if cmds.objExists(namelist)==False:
                namelistInValid.append(namelist)
    else:
        namelistInValid.append("catch_all")
    return namelistInValid