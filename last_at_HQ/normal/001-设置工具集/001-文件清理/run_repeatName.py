#!/usr/bin/env python
#coding=cp936
#coding=utf-8

#********************
#制作人：傅凯晖
#制作日期：2014.11.26
#********************

import maya.cmds as cmds
import maya.mel as mel

class F_Name_Dict:
    def F_name_dict(self):
        transform_type=[]
        transform_nodes_name={}
        transform_type=cmds.ls(typ="transform",s=True)
        for i in transform_type:
            transform_type_split=i.split('|')
            if transform_nodes_name.has_key(transform_type_split[-1]):
                transform_nodes_name[transform_type_split[-1]].append(i)
            else:
                transform_nodes_name[transform_type_split[-1]]=[i]
        self.transform_nodes_name=transform_nodes_name
        
    def F_find_repeatName(self):
        repeat_obj=[]
        for k in self.transform_nodes_name:
            if len(self.transform_nodes_name[k])>1:
                repeat_obj.append(k)
        return repeat_obj
        
    def F_list_select(self):
        repeat_objs=cmds.textScrollList ('repeat_list',q=True,si=True)
        obj_namespace=[]
        is_renamed=[]
        objs_namespace=''
        transform_type_namespace=repeat_objs[0].split(':')
        repeat_obj=transform_type_namespace[-1]
        for x in xrange(len(transform_type_namespace)-1):
            obj_namespace.append(transform_type_namespace[x])
            if len(obj_namespace)>1:
                objs_namespace=':'.join(obj_namespace)+':'
            else:
                objs_namespace=obj_namespace[0]+':'
        cmds.select(cl=True)
        for i in self.transform_nodes_name[objs_namespace+repeat_obj]:
            if cmds.objExists(i):
                cmds.select(i,add=True)
            else:
                is_renamed.append(i)
        for i in is_renamed:
            self.transform_nodes_name[objs_namespace+repeat_obj].remove(i)
        if len(self.transform_nodes_name[objs_namespace+repeat_obj])<2:
            cmds.textScrollList ('repeat_list',e=True,ri=(objs_namespace+repeat_obj))
            cmds.select(cl=True)
        if cmds.window('outlinerPanel1Window',q=True,exists=True):
            cmds.showWindow("outlinerPanel1Window")
        else:
            mel.eval("OutlinerWindow;")
            
fukh=F_Name_Dict()

def F_window():
    fukh.F_name_dict()
    repeat_obj=fukh.F_find_repeatName()
    if cmds.window('find_repeatname',q=True,exists=True):
        cmds.deleteUI('find_repeatname')
    cmds.window('find_repeatname',t='查找重复命名')
    cmds.formLayout('form')
    cmds.button('b2',l='刷新',c='F_window()')
    cmds.textScrollList('repeat_list',allowMultiSelection=True,append=repeat_obj,showIndexedItem=4,sc="fukh.F_list_select()")
    cmds.formLayout('form',edit=True,
    attachForm=[('repeat_list',"top",5),('repeat_list',"left",5),('b2',"left",5),('b2',"bottom",5),('b2',"right",5)],
    attachControl=('repeat_list',"bottom",5,'b2'),
    attachPosition=('repeat_list',"right",5,100),
    attachNone=('b2',"top"))
    cmds.showWindow('find_repeatname')

F_window()