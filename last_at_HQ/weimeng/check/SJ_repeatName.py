#coding=cp936
#coding=utf-8
#重命名的名字：repeatName().keys()
#重命名名字的节点列表：repeatName().values()
import pymel.core as pm
def rpname():
    allnodedicts = dict([[a,a.split("|")[-1]] for a in pm.ls()])
    repeatname ={}
    if len(allnodedicts.values())!=len(list(set(allnodedicts.values()))):
        for  k in range(len(allnodedicts.keys())):
            if allnodedicts.values().count(allnodedicts.values()[k])>1:
                if allnodedicts.values()[k] not in repeatname.keys():
                    repeatname[allnodedicts.values()[k]] =[allnodedicts.keys()[k]]
                else:
                    repeatname[allnodedicts.values()[k]].append(allnodedicts.keys()[k])
    return repeatname
   
if __name__=="__main__":
    print rpname().values()