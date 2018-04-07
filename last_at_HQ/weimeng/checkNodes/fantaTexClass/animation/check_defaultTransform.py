#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:libin
#--date--:2017-06-13
import maya.cmds as cmds
def check_defaultTransform():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'���λ����ת�����Ƿ��ʼ��'}
    '''
    sels= list(set(cmds.ls(type="transform"))-set(["persp","top","front","side"]))
    vails = ["tx","ty","tz","rx","ry","rz"]
    novails = ["sx","sy","sz"]
    attNoright = []
    for sel in sels:
        for vail in vails:
            attr = cmds.getAttr(sel+"."+vail)
            if attr!=0:
                attNoright.append(sel+"."+vail)
        for novail in novails:
            attr = cmds.getAttr(sel+"."+novail)
            if attr!=1:
                attNoright.append(sel+"."+novail)
    return attNoright

if __name__=='__main__':
    adj = check_defaultTransform()
    if adj!=[]:
        print  "λ����ת����δ��ʼ��"
    else:
        print  "λ����ת�����ѳ�ʼ��"