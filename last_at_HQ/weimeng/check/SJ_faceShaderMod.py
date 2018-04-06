#coding=cp936
#coding=utf-8

'''
������ʧ����ģ�ͣ�ck_missshader()
�������渳�����ģ�ͣ�ck_faceshader()

'''
import pymel.core as pm
#���ģ�顾������ʽ��[��ʧ����ģ��,...],[���渳��ģ��,...]��
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

#������ʧ����ģ��
def ck_missshader():
    return ck_meshcheck()[0]

#�������渳�����ģ��
def ck_faceshader():
    return ck_meshcheck()[1]

if __name__=="__main__":
    print ck_missshader()
