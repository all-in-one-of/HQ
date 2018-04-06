#coding=cp936
#coding=utf-8
'''
贴图处理模块（包括file节点，yeti毛发节点，变体节点的贴图处理）
贴图检查类（texCheckClass）：
    反馈贴图文件夹路径列表【反馈格式：[贴图文件夹路径,......]】：ck_texdirlists()
    反馈贴图节点及贴图路径列表【反馈格式：[{丢失贴图节点：贴图路径},......]】：ck_texpathlists()
    反馈丢失贴图文件夹路径列表【反馈格式：[贴图文件夹路径,......]】：ck_miss_texdirlists()
    反馈丢失贴图节点及贴图路径列表【反馈格式：[{丢失贴图节点：贴图路径},......]】：ck_miss_texpathlists()
    反馈丢失贴图节点及贴图路径列表【反馈格式：[贴图节点,......]】:texonODisk()    
'''
import pymel.core as pm
import os
yetinum =1
if pm.pluginInfo("pgYetiMaya",q=1,loaded=1,name=1)==0:
    try:
        pm.loadPlugin("pgYetiMaya")
    except:
        yetinum=0
        print "没有安装yeti插件！！",
class texCheckClass ():
    #获取所有贴图路径
    def getPath(self,filenode):
        nmfilepath  ={}
        mulfilepath  = {}
        if pm.nodeType(filenode)=="file":
            if pm.listConnections(filenode,d=0,type="choice")==[]:
                nmfilepath[filenode]=pm.getAttr(filenode+".fileTextureName").replace("\\","/")
            else:
                userattr =  pm.listAttr(filenode,ud=1)
                userattrpath = {}
                for u in range(len(userattr)):
                    if userattr[u][:3]=="Tex":
                        userattrpath[userattr[u]] = pm.getAttr(filenode +"."+userattr[u]).replace("\\","/")
                mulfilepath[filenode] = userattrpath
        else:
            try:
                nofiles = filenode.getShape()
            except:
                nofiles=filenode
            if nofiles!=[]:
                if yetinum==1:
                    pgyetitexs = pm.pgYetiGraph(pm.PyNode(nofiles),listNodes=True,type="texture")                
                    if pgyetitexs !=None:
                        yetipaths = {}
                        yetipathsudim ={}
                        for p in range(len(pgyetitexs)):
                            yetipath = pm.pgYetiGraph(nofiles,node=pgyetitexs[p],param="file_name",getParamValue=True)
                            if yetipath[-10:-4].upper() !="<UDIM>":
                                yetipaths[pgyetitexs[p]]=yetipath
                            else:
                                yetipathsudim[pgyetitexs[p]]=yetipath
                        if yetipaths!={}:
                            nmfilepath[nofiles] = yetipaths
                        if yetipathsudim!={}:
                            mulfilepath[nofiles] = yetipathsudim
                else:
                    pass
                    
        return nmfilepath,mulfilepath
    #检查贴图是否存在    
    def checkExs(self,checknode,checkpath,checkex,checknoex):
        if os.path.splitext(os.path.basename(checkpath))[0][-6:].upper()!="<UDIM>":
            if os.path.exists(checkpath):
                if checkex.has_key(os.path.dirname(checkpath))==False:
                    checkex[os.path.dirname(checkpath)] = {checknode:checkpath}
                else:
                    checkex[os.path.dirname(checkpath)].update({checknode:checkpath})
            else:
                if checknoex.has_key(os.path.dirname(checkpath))==False:
                    checknoex[os.path.dirname(checkpath)] = {checknode:checkpath}
                else:
                    checknoex[os.path.dirname(checkpath)].update({checknode:checkpath})
        else:
            cklists = os.listdir(os.path.dirname(checkpath))
            for cklist in cklists:
                if os.path.splitext(cklist)[0][:-4] ==os.path.splitext(os.path.basename(checkpath))[0][:-6]:
                    if os.path.exists( os.path.dirname(checkpath)+"/"+cklist):
                        if checkex.has_key(os.path.dirname(checkpath))==False:
                            checkex[os.path.dirname(checkpath)] = {checknode:checkpath}
                        else:
                            checkex[os.path.dirname(checkpath)].update({checknode:checkpath})
                    else:
                        if checknoex.has_key(os.path.dirname(checkpath))==False:
                            checknoex[os.path.dirname(checkpath)] = {checknode:checkpath}
                        else:
                            checknoex[os.path.dirname(checkpath)].update({checknode:checkpath})
        return checkex,checknoex
    #检查所有节点及贴图路径    
    def checkTexPath(self):
        if yetinum==1:
            filewholes = pm.ls(type="file")+[u for u in pm.ls(type="pgYetiMaya") if pm.pgYetiGraph(u,listNodes=True,type="texture") !=[]]  
        else:
            filewholes = pm.ls(type="file")
        global existspath
        global noexistpath
        existspath = {}
        noexistpath ={}
        for filewhole in filewholes:
            ##非多贴图
            if  texCheckClass().getPath(filewhole)[0] !={}:
                texnode =  texCheckClass().getPath(filewhole)[0]
                for texpath in texnode.values():
                    if type(texpath)!=type({}):
                        filename =  os.path.basename(texpath)
                        dirname = os.path.dirname(texpath)
                        ##一般贴图
                        if texnode.keys()[0].getAttr("uvTilingMode")==0:
                            texCheckClass().checkExs(texnode.keys()[0],texpath,existspath,noexistpath)
                        ##UDIM
                        elif texnode.keys()[0].getAttr("uvTilingMode")==3:
                            texCheckClass().checkExs(texnode.keys()[0],texpath,existspath,noexistpath)
                        else:
                            print "not be supported UVTiling Mode!!",
                    else:
                        if yetinum==1:
                            ##yeti的非udim
                            for y in range(len(texnode.keys())):
                                yetitex = texnode.values()[y]
                                for t in range(len(yetitex.keys())):
                                    texCheckClass().checkExs(texnode.keys()[y],yetitex.values()[t],existspath,noexistpath)
                        else:
                            pass
            ##多贴图
            if texCheckClass().getPath(filewhole)[1] !={}:
                multinode =  texCheckClass().getPath(filewhole)[1]
                for e in range(len(multinode.values())):
                    texattr =  multinode.values()[e]
                    if pm.nodeType(multinode.keys()[e])=="file":
                        for x in range(len(texattr.keys())):
                            texCheckClass().checkExs(multinode.keys()[e],texattr.values()[x],existspath,noexistpath)
                    else:
                        if yetinum==1:
                            ##yeti的udim
                            texattr =  multinode.values()[e]
                            for r in range(len(texattr.keys())):
                                texCheckClass().checkExs(multinode.keys()[e],texattr.values()[r],existspath,noexistpath)
                        else:
                            pass
        return existspath,noexistpath

        
#反馈贴图文件夹路径列表
def ck_texdirlists():
    return texCheckClass().checkTexPath()[0].keys()
    
#反馈贴图节点及贴图路径列表
def ck_texpathlists():
    return texCheckClass().checkTexPath()[0].values()
    
#反馈丢失贴图文件夹路径列表
def ck_miss_texdirlists():
    return texCheckClass().checkTexPath()[1].keys()
    
#反馈丢失贴图节点及贴图路径列表
def ck_miss_texpathlists():
    return texCheckClass().checkTexPath()[1].values()
    
#反馈不在o盘贴图节点列表
def texonODisk():
    texex =  []
    if texCheckClass().checkTexPath()[0]!=[]:
        fullpaths =  texCheckClass().checkTexPath()[0].keys()
        for f in range(len(fullpaths)):
            if fullpaths[f].split(":")[0].upper()!="O":
                texex= texex+texCheckClass().checkTexPath()[0].values()[f].keys()
            else:
                pass
    return texex

if __name__ == "__main__":
        print texonODisk()