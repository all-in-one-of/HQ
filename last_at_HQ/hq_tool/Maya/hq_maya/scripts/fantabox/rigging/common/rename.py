#!/usr/bin/env python
#coding=cp936
#coding=utf-8

#********************
#制作人：傅凯晖
#制作日期：2014.12.11
#********************

import maya.cmds as cmds

def rename_window():
    if cmds.window('rename_shape',q=True,exists=True):
        cmds.deleteUI('rename_shape')
    cmds.window('rename_shape',t='rename')
    cmds.columnLayout()
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(80, 75), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
    cmds.text(l='name:')
    cmds.textField('name',w=400,h=20,enterCommand='rename_transform()')
    cmds.setParent( '..' )
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(200,200), adjustableColumn=2, columnAlign=(50, 'right'), columnAttach=[(1, 'both', 30), (2, 'both', 30)] )
    cmds.button('b1',l='改transform',c='rename_transform()')
    cmds.button('b2',l='改shapes',c='rename_shapes()')
    cmds.setParent( '..' )
    cmds.showWindow('rename_shape')

def rename_transform():
    name=cmds.textField('name',q=True,text=True)
    transform_type=[]
    new_name=[]
    num_transform=[]
    cmds.select(hi=True)
    transform_type=cmds.ls(sl=True,typ="transform")
    transform_type_1=[]
    node_Type_1=[]
    node_Type=[]
    for z in transform_type:
        node_Type_1.append(cmds.nodeType(z))
    node_Type=set(node_Type_1).remove('transform')
    for n in transform_type:
        if cmds.nodeType(n) in node_type:
            transform_type_1.append(n)
    for y in transform_type_1:
        transform_type.remove(y)
    #########################################################
    obj_namespace=[]
    objs_namespace=''
    transform_type_namespace=transform_type[0].split(':')
    for x in xrange(len(transform_type_namespace)-1):
        obj_namespace.append(transform_type_namespace[x])
        if len(obj_namespace)>1:
            objs_namespace=':'.join(obj_namespace)+':'
        else:
            objs_namespace=obj_namespace[0]+':'
    
    #########################################################
    new_name_all=[]
    for i in xrange(len(transform_type)):
        transform_type_split=transform_type[i].split('|')
        if i==0:
            transform_type_split[-1]=objs_namespace+name
        else:
            transform_type_split[-1]=objs_namespace+name+str(i)
        new_name_split=('|').join(transform_type_split)
        new_name_all.append(new_name_split)
        new_name.append(transform_type_split[-1])
        num_transform.append(i)
    
    num_transform.reverse()
        
    for k in num_transform:
        cmds.rename(transform_type[k],new_name[k])
    cmds.select(new_name[0])
    rename_shapes()
    rename_constraint()
        
def rename_shapes():
    now_select=cmds.ls(sl=True)
    cmds.select(hi=True)
    shape_type=cmds.ls(sl=True,s=True)
    transform_name_1={}
    for y in shape_type:
        transform_name=cmds.listRelatives(y,p=True)[0]
        y_split=y.split('|')
        short_transform_name=transform_name.split('|')
        if transform_name in transform_name_1:
            if y_split[-1]!=(short_transform_name[-1]+"Shape_"+transform_name_1[transform_name]):
                if not cmds.objExists(short_transform_name[-1]+"Shape_"+transform_name_1[transform_name]):
                    cmds.rename(y,(short_transform_name[-1]+"Shape_"+transform_name_1[transform_name]))
            transform_name_1[transform_name]=transform_name_1[transform_name]+1
        else:
            transform_name_1[transform_name]=1
            if y_split[-1]!=(short_transform_name[-1]+"Shape"):
                if not cmds.objExists(short_transform_name[-1]+"Shape"):
                    cmds.rename(y,(short_transform_name[-1]+"Shape"))
    cmds.select(now_select)
    
def rename_constraint():
    transform_type=[]
    num_transform=[]
    now_select=cmds.ls(sl=True)
    cmds.select(hi=True)
    transform_type=cmds.ls(sl=True,typ="transform")
    transform_type_1=[]
    node_type_1=[]
    node_type=[]
    for z in transform_type:
        node_type_1.append(cmds.nodeType(z))
    node_type=list(set(node_type_1))
    node_type.remove('transform')
    for n in transform_type:
        if cmds.nodeType(n) in node_type:
            transform_type_1.append(n)
    if transform_type_1 !=[]:
        for y in transform_type_1:
            transform_name=cmds.listRelatives(y,p=True)[0]
            transform_name_split=transform_name.split('|')
            y_split=y.split('|')
            y_split_1=y_split[-1].split('_')
            if y_split[-1]!=transform_name_split[-1]+'_'+y_split_1[-1]:
                cmds.rename(y,transform_name_split[-1]+'_'+y_split_1[-1])
    
    cmds.select(now_select)
#def rename():
if __name__=='__main__':
    rename_window()
