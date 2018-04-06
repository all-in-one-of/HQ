#coding=cp936
#coding=utf-8

'''
反馈丢失材质模型：ck_missshader()
反馈按面赋予材质模型：ck_faceshader()

'''
import pymel.core as pm
#检查模块【反馈格式：[丢失材质模型,...],[按面赋予模型,...]】
def ck_meshcheck():
    meshsels = pm.ls(type="mesh")
    faceshadermesh =[]
    missfacemesh = []
    for meshsel in meshsels:
        sgs = list(set(pm.listConnections(meshsel,type="shadingEngine")))
        if sgs!=[]:
            for sg in sgs:
                plugs = pm.listConnections(sg,type="mesh",plugs=1)
                for plug in plugs:
                    if plug.find("objectGroups")!=-1:
                        if meshsel not in faceshadermesh:
                            faceshadermesh.append(meshsel)
        else:
            if meshsel not in missfacemesh:
                missfacemesh.append(meshsel)
    return missfacemesh,faceshadermesh 

#反馈丢失材质模型
def ck_missshader():
    return ck_meshcheck()[0]

#反馈按面赋予材质模型
def ck_faceshader():
    return ck_meshcheck()[1]

if __name__=="__main__":
    print ck_missshader()
