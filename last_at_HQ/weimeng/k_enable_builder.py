#coding:utf-8
__author__ = 'Administrator'
import json
import os
import shutil
#N为common（普通），R为rig（设置），C为cluster（角色），M为model（模型），A为animation（动画），F为fx（特效），L为lighting（灯光组装），HQ为华强
path = 'C:/Users/dengtao/Documents/maya/2015-x64/scripts/fantaTexClass'
menuDatas = {"k005_check_wkHeadsUp": [1, "true", "检查wkHeadsUp", "common", "通用",["N"]],
"k007_check_UNKNOWNREF": [1, "true", "检查UNKNOWNREF节点", "common", "通用",["N"]],
"k008_check_unknown": [1, "true", "检查未知节点", "common", "通用",["N"]], 
"k009_check_sharedRef": [1, "true", "检查sharedReferenceNode节点", "common", "通用",["N"]],
"k011_check_Opathref": [1, "true", "检查不在O盘的参考路径", "common", "通用",["N"]], 
"k016_check_uuoig": [1, "true", "检查检查多余的oig节点", "common", "通用",["N"]],  
"check_display_wireframe": [1, "true", "检查提交文件的视窗是否为线框模式", "common", "通用",["N"]],
"check_invalid_displayLayer": [1, "true", "检查多余显示层", "common", "通用",["N"]],
"check_catchName": [1, "true", "检查动捕提交文件名字规范", "common", "通用",["RtoHQ"]], 
"check_cluster_meshOnly": [1, "true", "检查群集文件模型组是否干净", "common", "通用",["RtoC"]], 
"check_listJoint_ExGroup": [1, "true", "检查群集文件是否存在空组", "common", "通用",["RtoC"]], 
"k002_check_novertPolo": [1, "true", "检查无点的Plolygons", "modeling", "模型",["MtoR"]], 
"k004_check_vshapeNode": [1, "fasle", "检查不正确的shape命名", "modeling", "模型",["MtoR"]],
"check_aiSubdiv": [1, "true", "检查Arnold渲染细分大于3的物体", "modeling", "模型",["MtoR"]],
"k015_check_displink": [1, "true", "检查连接断了的置换节点", "modeling", "模型",["N"]], 
"k003_check_History": [1, "fasle", "检查绑定后不干净的shape", "rigging", "设置",["RtoA"]],
"check_defaultTransform": [1, "true", "检查位移旋转缩放是否初始化", "animation", "动画",["MtoR"]],  
"k010_check_Opathvray": [1, "true", "检查不在O盘的Vray代理路径", "fx", "特效",["MtoR"]], 
"k012_check_OpathCache": [1, "true", "检查不在O盘的布料及几何体缓存路径", "fx", "特效",["FtoL"]],
"k013_check_Opathaisin": [1, "true", "检查不在O盘的arnold代理路径", "fx", "特效",["MtoR","L","AtoL","FtoL"]], 
"k014_check_Opathabc": [1, "true", "检查不在O盘的abc代理路径", "fx", "特效",["AtoL","FtoL"]], 
"k001_check_hairlinkarnold": [1, "fasle", "检查没有连接arnold的毛发节点", "fx", "特效",["MtoR","RtoA","AtoL","FtoL"]],
"k006_check_voronoi": [1, "true", "检查voronoi破碎节点", "fx", "特效",["FtoL"]],
"check_render_Options": [1, "true", "检查Options设置是否正确", "rendering", "组装",["L"]],
"check_renderLayer": [1, "true", "检查多余渲染层", "rendering", "组装",["AtoL"]],
"check_feetMask": [1, "true", "检查脚底板", "rendering", "组装",["AtoL"]]
}

subpaths=[]
maindirs = [a for a in os.listdir(path) if len(a.split("."))==1]
for maindir in maindirs:
    subdirs = path+"/"+maindir
    subfiles =[b for b in  os.listdir(subdirs) if b.split(".")[-1]=="py"]
    subtexts = []
    for subfile in subfiles:
        subpath = subdirs+"/"+ subfile
        subpaths.append(subpath)
        print subpath
        filenames = subfile.split('.')[0]
        if filenames !="__init__":
            subtexts.append("from "+filenames+" import *")
    fl=open(subdirs+'/__init__.py', 'w')
    for subtext in subtexts:
        fl.write(subtext)
        fl.write("\t\n")
    fl.close()

for menuData in menuDatas:
    newdir= path+"/"+menuDatas[menuData][3]
    newpath = newdir+"/"+ menuData+".py"
    if os.path.exists(newpath)==False:
        oldpath  = [c for c in subpaths if c.split("/")[-1]==menuData+".py"]
        shutil.move(oldpath[0],newpath)
    else:
        pass


dd = json.dumps( menuDatas, indent=4 )

file = open('E:/work/7_0616_CheckNode/k_enable.json', 'w')
file.write(dd)
file.close()
