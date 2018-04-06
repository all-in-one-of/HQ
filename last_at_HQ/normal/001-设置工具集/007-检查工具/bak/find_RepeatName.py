#!/usr/bin/env python
#coding=cp936
#coding=utf-8

import maya.cmds as cmds

def F_find_repeatName():
    transform_type=[]
    repeat_obj=[]
    transform_type=cmds.ls(typ="transform",s=True)
    
    for i in range(len(transform_type)):
        transform_type_split=transform_type[i].split('|')
        transform_type[i]=transform_type_split[-1]
    
    for i in range(len(transform_type)):
        if transform_type.count(transform_type[i])>1:
            if transform_type[i] not in repeat_obj:
                repeat_obj.append(transform_type[i])
    return repeat_obj
            
def F_window():   
    repeat_obj=F_find_repeatName()
    if cmds.window('find_repeatname',q=True,exists=True):
        cmds.deleteUI('find_repeatname')
    cmds.window('find_repeatname',t='查找重复命名')
    cmds.formLayout('form')
    cmds.button('b2',l='刷新',c='F_new()')
    cmds.textScrollList('repeat_list', allowMultiSelection=True,append=repeat_obj,showIndexedItem=4,sc="F_list()")
    cmds.formLayout('form',edit=True,attachForm=[('repeat_list',"top",5),('repeat_list',"left",5),('b2',"left",5),('b2',"bottom",5),('b2',"right",5)],attachControl=('repeat_list',"bottom",5,'b2'),attachPosition=('repeat_list',"right",5,100),attachNone=('b2',"top"))
    cmds.showWindow('find_repeatname')

def F_new():
    F_find_repeatName()
    cmds.textScrollList('repeat_list',e=True,ra=True)
    F_window()

def F_list():
    repeat_objs=cmds.textScrollList ('repeat_list',q=True,si=True)
    cmds.select('*'+repeat_objs[0])
    
F_window()