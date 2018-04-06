#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai'
buttonDir = {
    'bt001_generalCheckButton':[u'通用检查','generalCheckWidget'] ,
    'bt002_pathCheckButton':[u'路径检查','pathCheckWidget'] ,
    'bt003_fileCheckButton':[u'文件检查','fileCheckWidget'],
    'bt004_newCheckButton':[u'新检查','newCheckWidget']
}
checkBoxDir = {
    'cb001_checkBox': [buttonDir.keys().index('bt001_generalCheckButton'), 'checkBox'],
    'cb002_checkBox': [buttonDir.keys().index('bt001_generalCheckButton'), 'checkBox'],
    'cb003_checkBox': [buttonDir.keys().index('bt001_generalCheckButton'), 'checkBox'],
    'cb004_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'), 'checkBox'],
    'cb005_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'), 'checkBox'],
    'cb006_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'), 'checkBox'],
    'cb007_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'), 'checkBox'],
    'cb008_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'), 'checkBox'],
    'cb009_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'),u'中文测试'],
    'cb010_checkBox': [buttonDir.keys().index('bt003_fileCheckButton'), 'checkBox'],
    'cb011_checkBox': [buttonDir.keys().index('bt003_fileCheckButton'), 'checkBox'],
    'cb012_checkBox': [buttonDir.keys().index('bt003_fileCheckButton'), 'checkBox'],
    'cb013_checkBox': [buttonDir.keys().index('bt003_fileCheckButton'), 'checkBox'],
    'cb014_checkBox': [buttonDir.keys().index('bt003_fileCheckButton'), 'checkBox'],
    'cb015_checkBox': [buttonDir.keys().index('bt004_newCheckButton'), 'checkBox'],
    'cb016_checkBox': [buttonDir.keys().index('bt004_newCheckButton'), 'checkBox'],
    'cb017_checkBox': [buttonDir.keys().index('bt004_newCheckButton'), 'checkBox'],
    'cb018_checkBox': [buttonDir.keys().index('bt004_newCheckButton'), 'checkBox'],
}