#!/usr/bin/python
# -*- coding : utf-8 -*-
#--author-- : yujing,xusijian
#--date-- : 2017.6.20
import maya.cmds as cmds
#######---- "Mesh" ---- ############# 
def check_cluster_meshOnly():
    vaillist = ["adv_Hips","front","persp","side","top"]
    faGeogrp = [x for x in cmds.ls(type="transform") if cmds.listRelatives(x,p=1,type='transform')==None and x not in vaillist]
    invalid = []
    for g in faGeogrp:
        if cmds.listRelatives(g,c=1,type="mesh")==None:
            faadj = cmds.listRelatives(g,ad=1)
            try:
                childGeogrp =[ {c:cmds.nodeType(c)} for c in faadj]
            except:
                childGeogrp = []
            fageoall = [m.keys()[0] for m in childGeogrp if m.values()[0]=="mesh"]
            childtrans = [n.keys()[0] for n in childGeogrp if n.values()[0]=="transform" and cmds.listRelatives(n.keys()[0],c=1,type="mesh")!=None]
            diffs = [a for a in faadj if a not in childtrans and a not in fageoall]
            if diffs!=[]:
                diffs=list(set(diffs))
            for diff in diffs:
                try:
                    if cmds.nodeType(diff)=="transform":
                        invalid.append(diff)
                    else:
                        difftr =  cmds.listRelatives(diff,p=1,type="transform")
                        if difftr!=[]:
                            invalid+=difftr
                except:
                    invalid.append(0)
        else:
            invalid.append(g)
    if invalid!=[]:
        if 0 not in invalid:
            invalid = list(set(invalid))
        else:
            invalid=['not a pure ClusterFile!!']
    return invalid