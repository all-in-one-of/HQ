#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai'
buttonDir = {
    'bt001_generalCheckButton':[u'ͨ�ü��','generalCheckWidget'] ,
    'bt002_pathCheckButton':[u'·�����','pathCheckWidget'] ,
    'bt003_fileCheckButton':[u'�ļ����','fileCheckWidget'],
    'bt004_newCheckButton':[u'�¼��','newCheckWidget']
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
    'cb009_checkBox': [buttonDir.keys().index('bt002_pathCheckButton'),u'���Ĳ���'],
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