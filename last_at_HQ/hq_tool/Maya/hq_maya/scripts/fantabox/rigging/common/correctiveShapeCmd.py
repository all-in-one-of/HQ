#!usr/bin/env python
#coding:utf-8
"""
@Amend Time: 2017.4.25

@author: wangzhi
"""
import maya.cmds as cmds
import pathforuser
import sys

path = pathforuser.path_dir()
addPath = path+'common/scripts/'
if addPath not in sys.path:
	sys.path.append(addPath)


query=cmds.pluginInfo( addPath + 'shapeCorrect2015x64.mll', query=True ,loaded=True)
if query == 0:
	cmds.loadPlugin(addPath + 'shapeCorrect2015x64.mll')
import shapeCorrect;reload(shapeCorrect)
shapeCorrect.cort.correctiveShapeCmd()