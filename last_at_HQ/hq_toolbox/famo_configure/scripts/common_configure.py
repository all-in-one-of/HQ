#coding:utf-8
__author__ = 'Xusijian'
__date__    = '2017-08-21'
'''
说明：所有版本都有此脚本生成配置exe；注意一下几点要求：
1.脚本名必须与模块名字一致，如common_configure_local.py与common_configure_local.mod
2.本地版需要在脚本名后加“_local”,如：common_configure_local
3.机房版需要在脚本名后加“_renderFarm”，如：common_configure_renderFarm
4.自动更新脚本则需要在脚本名后加“_update”,如：common_configure_local_update
'''

import os
import sys
from PySide import  QtGui
import time
import subprocess
import json
import getpass

mainpaths = r"O:/hq_tool"

##获取我的文档
def documentsLocation():    
    handle = subprocess.Popen('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"  /v personal', shell=True, stdout=subprocess.PIPE)
    hostid = handle.communicate()[0]
    handle.kill
    return hostid.split( 'REG_SZ')[1].strip().replace("\\","/")

##升级同步模块
class HQ_tool():
    def __init__(self):
        try:
            self.hostdir = documentsLocation()
        except:
            self.hostdir = "C:/Users/"+getpass.getuser()+"/Documents"
        self.modulespath= self.hostdir+r'/maya/modules'
        self.mayaver = [r"/maya/2015-x64",r"/maya/2013-x64",r"/maya/2017"]
        self.mainpath = r"C:/hq_tool"
        self.mainpatho = mainpaths
        self.rendererDesc = [self.mainpatho+r"/Maya/Arnold/Arnold_1.2.7.3_Maya2015/arnoldRenderer.xml",self.mainpatho+r"/Maya/Vray/vray_3.10.01_Maya2015/vrayRenderer.xml",self.mainpatho+r"/Maya/Arnold/Arnold_1.0.0.1_Maya2013/arnoldRenderer.xml",self.mainpatho+r"/Maya/Vray/vray_2.40.01_Maya2013/vrRenderer.xml"]
        self.mayamain = r"C:/Program Files/Autodesk"
    def Doitcmd(self,srfile,trfile,mode):
        if mode=="copy":
            try:
                if os.path.isdir(srfile)==False:
                    trdir = os.path.dirname(trfile)
                    if os.path.exists(trdir)==False:
                        mkcmd = 'md "%s" '%(trdir.replace("/","\\"))
                        subprocess.Popen(mkcmd,shell=True)
                    if os.path.exists(trfile):
                        delfilecmd = 'del /s "%s" '%(trfile.replace("/","\\"))
                        subprocess.Popen(delfilecmd,shell=True)
                    cpcmd = 'copy  "%s" "%s"'%(srfile.replace("/","\\"),trfile.replace("/","\\"))
                    cmdout = subprocess.Popen(cpcmd,shell=True)
                    (stdout, stderr) = cmdout.communicate()
                    return stdout
                else:
                    if os.path.listdir(srfile)==[]:
                        mkcmd = 'md "%s" '%(trdir.replace("/","\\"))
                        subprocess.Popen(mkcmd,shell=True)
                        (stdout, stderr) = cmdout.communicate()
                        return stdout

            except:
                return  srfile+"'s copy error!!"

    def updateVer(self,path):
        HQ_tool().Doitcmd(path,self.modulespath+r"/foma_plugins.mod","copy")

    def initsetup(self):
        dirlist = []
        modulesdirs = [self.hostdir+r"/maya/modules",self.hostdir+r"/maya/2015-x64/modules",r"C:/Program Files/Autodesk/Maya2015/modules",self.hostdir+r"/maya/2013-x64/modules",r"C:/Program Files/Autodesk/Maya2013/modules"]
        tarlist =["mtoa.mod","pgYetiMaya.mod","VRayForMaya.module","shaveHaircut.mod"]
        for modulesdir in modulesdirs:
            if os.path.exists(modulesdir):
                dirlistpath  = [modulesdir+"/"+i for i in os.listdir(modulesdir) if  i  in tarlist]
                dirlist = dirlist+dirlistpath
            if dirlist !=[]:
                for r in dirlist:
                    try:
                        os.remove(r)
                    except:
                        pass
            else:
                pass

        for rendererDesc in self.rendererDesc:
            maver = rendererDesc.split("/")[-2][-4:]
            HQ_tool().Doitcmd(rendererDesc, self.mayamain+r"/Maya"+maver+"/bin/rendererDesc/"+os.path.basename(rendererDesc),"copy")
        for mayavers in self.mayaver:
            if os.path.exists( self.hostdir+mayavers):
                if os.path.exists( self.hostdir+mayavers+r"/maya.env"):
                    oldenv = open(self.hostdir +mayavers+r"/maya.env", 'r')
                    oldtxt = oldenv.readlines()
                    oldenv.close()
                    if  oldtxt !=[]:
                        adj = []
                        for lin in oldtxt:
                            if lin.find("Yeti")!=-1:
                                adj.append(lin)
                            if lin.find("VRAY")!=-1:
                                adj.append(lin)
                            if lin.find("mtoadeploy") != -1:
                                adj.append(lin)
                        if adj!=[]:
                            HQ_tool().Doitcmd(self.hostdir + mayavers+r"/maya.env",self.hostdir + mayavers+r"/maya_bak.env","copy")
                            file = open(self.hostdir+mayavers+r"/maya.env", 'w')
                            blank = ""
                            file.write(blank)
                            file.close()
                        else:
                            pass
                    else:
                        pass
                else:
                    file = open(self.hostdir+mayavers+r"/maya.env", 'w')
                    blank = ""
                    file.write(blank)
                    file.close()
            else:
                pass

            copypaths = {self.mainpath+r"/Maya/Shave/shave_1.1_maya2015/bin/Cg/shaveHair.cgfx": self.mayamain+r"/Maya2015/bin/Cg/shaveHair.cgfx",self.mainpath+r"/Maya/Shave/shave_1.1_maya2013/bin/libShave.dll": self.mayamain+r"/Maya2013/bin/libShave.dll",self.mainpath+r"/Maya/Shave/shave_1.1_maya2013/bin/libShaveAPI.dll": self.mayamain+r"/Maya2013/bin/libShaveAPI.dll"}
            for copypath in copypaths.keys():
                if os.path.exists(copypaths[copypath]) == False:
                    HQ_tool().Doitcmd(copypath, copypaths[copypath],"copy")
                else:
                    pass
##本地化模块
class localize():
    def __init__(self):
        self.errorfile = []
        self.walkdirsCMDRs = []
    def walkDirs_CMD(self,directory,dirmod):
        assert os.path.isdir(directory),'make sure directory argument should be a directory'
        if dirmod==1:
            cmd = 'dir /s /b /ad ' +'"' + directory.replace("/","\\")+'"'
        else:
            cmd = 'dir /s /b /a-d ' +'"'+ directory.replace("/","\\")+'"'
        cmdout = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = cmdout.communicate()
        self.walkdirsCMDRs=stdout.replace('\r\n',',').replace("\\","/").split(",")[:-2]
        if cmdout.wait() == 0:
            return self.walkdirsCMDRs
    def getPrettyTime(self,state):
        return time.strftime('%y-%m-%d %H:%M:%S', time.localtime(state.st_mtime)) 
    def Doitcmd(self,srfile,trfile,mode):
        if mode=="copy":
            try:
                if os.path.isdir(srfile)==False:
                    trdir = os.path.dirname(trfile)
                    if os.path.exists(trdir)==False:
                        mkcmd = 'md "%s" '%(trdir.replace("/","\\"))
                        subprocess.Popen(mkcmd,shell=True)
                    if os.path.exists(trfile):
                        delfilecmd = 'del /s "%s" '%(trfile.replace("/","\\"))
                        subprocess.Popen(delfilecmd,shell=True)
                    cpcmd = 'copy  "%s" "%s"'%(srfile.replace("/","\\"),trfile.replace("/","\\"))
                    cmdout = subprocess.Popen(cpcmd,shell=True)
                    (stdout, stderr) = cmdout.communicate()
                    return stdout,stderr
                else:
                    if os.path.listdir(srfile)==[]:
                        mkcmd = 'md "%s" '%(trdir.replace("/","\\"))
                        subprocess.Popen(mkcmd,shell=True)
                        (stdout, stderr) = cmdout.communicate()
                        return stdout,stderr
            except:
                return  srfile+"'s copy error!!"
    def splitInvaliddir(self,sppath):
        invaliddirs = ['programs','famo_configure']
        if list(set(invaliddirs)&set(sppath.split("/")))!=[]:
            return 1
        else:
            return 0
    def opan2local(self,srpath,tarpath,opanpaths,localpaths):
        invalidTypes =["db","inf"]
        dealfile=[]
        cFilelistjson = localpaths+"/hq_tool_filelists.json"
        oFilelistjson = opanpaths+"/hq_tool_filelists.json" 
        if  os.path.exists(cFilelistjson) and os.path.exists(oFilelistjson):
            if localize().getPrettyTime(os.stat(cFilelistjson))!=localize().getPrettyTime(os.stat(oFilelistjson)):
                if os.path.exists(srpath)==True:
                    if os.path.exists(tarpath)==True:
                        #o盘文件列表
                        odiskfilepathalllists= localize().walkDirs_CMD(srpath,0)
                        odiskfilepathlist=[b for b in odiskfilepathalllists if localize().splitInvaliddir(b)==0]
                        #c盘文件列表
                        if os.path.exists(tarpath)==True and localize().walkDirs_CMD(tarpath,0)!=None:
                            cdiskfilepathlists = localize().walkDirs_CMD(tarpath,0)
                            cdiskdirpathlists = localize().walkDirs_CMD(tarpath,1)
                        else:
                            cdiskfilepathlists=[]
                        #c盘有O盘没有
                        try:
                            delfile = [e for e in cdiskfilepathlists if os.path.exists(e.replace(tarpath,srpath))==False]
                            deldir = [e for e in cdiskdirpathlists if os.path.exists(e.replace(tarpath,srpath))==False]
                            delfilepathlists = delfile+deldir
                        except:
                            delfilepathlists = []
                        #排查非必要文件的O盘文件列表
                        odiskfilepathlists =[a for a in odiskfilepathlist if a.split("/")[-1].split(".")[-1] not in invalidTypes]
                        #o盘与c盘共存文件
                        commonfilelists =[b for b in odiskfilepathlists if os.path.exists(b.replace(srpath,tarpath))==True]
                        #o盘存在而c盘不存在的文件
                        updatefilelists = list(set(odiskfilepathlists)-set(commonfilelists))
                        #相同文件对比拷贝
                        
                        if commonfilelists!=[]:
                            for commonfilelist in commonfilelists:
                                if os.path.exists(commonfilelist.replace(srpath,tarpath)):
                                    if os.path.isdir(commonfilelist)==False:
                                        if localize().getPrettyTime(os.stat(commonfilelist))!=localize().getPrettyTime(os.stat(commonfilelist.replace(srpath,tarpath))):
                                            #copy commonfilelist（Odisk） To commonfilelist.replace(srpath,tarpath)（Cdisk）
                                            try:
                                                delfilecmd = 'del /s "%s" '%(commonfilelist.replace(srpath,tarpath).replace("/","\\"))
                                                subprocess.Popen(delfilecmd,shell=True)
                                                cpcmd = 'copy  "%s" "%s"'%(commonfilelist.replace("/","\\"),commonfilelist.replace(srpath,tarpath).replace("/","\\"))
                                                subprocess.Popen(cpcmd,shell=True)
                                                dealfile.append(commonfilelist)
                                            except:
                                                return  commonfilelist+"'s updatefile error!!"
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    print commonfilelist
                        if updatefilelists!=[]:
                            for updatefilelist in updatefilelists:
                                try:
                                    localize().Doitcmd(updatefilelist,updatefilelist.replace(srpath,tarpath),"copy")
                                    dealfile.append(updatefilelist)
                                except:
                                    return  updatefilelist+"'s copyfile error!!"    
                        if delfilepathlists!=[]:
                            for delfilepathlist in delfilepathlists:
                                if os.path.isdir(delfilepathlist)==False:
                                    #delete delfilepathlist
                                    try:
                                        delfilecmd = 'del /s "%s" '%(delfilepathlist.replace("/","\\"))
                                        subprocess.Popen(delfilecmd,shell=True)
                                        dealfile.append(delfilepathlist)
                                    except:
                                          return  delfilepathlist+"'s deletefile error!!"   
                                else:
                                    #delete delfilepathlist
                                    try:
                                        deldircmd = 'rd /s/q "%s" '%(delfilepathlist.replace("/","\\"))
                                        subprocess.Popen(deldircmd,shell=True)
                                        dealfile.append(delfilepathlist)
                                    except:
                                        return  delfilepathlist+"'s deletedir error!!"   
                        emptydirs = [d for d in localize().walkDirs_CMD(tarpath,1) if os.listdir(d)==[]]
                        for emptydir in emptydirs:
                            #delete emptydir
                            try:
                                deldircmd = 'rd /s/q "%s" '%(emptydir.replace("/","\\"))
                                subprocess.Popen(deldircmd,shell=True)
                            except:
                                return emptydir+"'s deleteEmptydir error!!" 
                    else:
                        try:
                            mkcmd = 'md "%s" '%(tarpath.replace("/","\\"))
                            subprocess.Popen(mkcmd,shell=True)
                            cpcmd = 'xcopy "%s" "%s" /s /f /h'%(srpath.replace("/","\\"),tarpath.replace("/","\\"))
                            subprocess.Popen(cpcmd,shell=True)
                        except:
                            return "rootdir's Allcopy error!!" 
                    localize().Doitcmd(oFilelistjson,cFilelistjson,"copy")
                else:
                    return "sourceDir not exists!!"
        else:
            return "hq_tool_filelists.json 丢失！！"

##清理本地多余文件
def earseCdirsCmd():
    earseCdirs =["C:/hq_tool/programs","C:/hq_tool/famo_configure"]
    for earseCdir in earseCdirs:
        deldircmd = 'rd /s/q "%s" '%(earseCdir.replace("/","\\"))
        subprocess.Popen(deldircmd,shell=True)

##配置完成提示
class finishbar(QtGui.QWidget):
    def __init__(self):
        super(finishbar, self).__init__()
        try:
            self.hostdir = documentsLocation()
        except:
            self.hostdir = "C:/Users/"+getpass.getuser()+"/Documents"
        self.modulespath= self.hostdir+r'/maya/modules'
        self.initUI()
    def initUI(self):
        if os.path.exists(self.modulespath+ r"\foma_plugins.mod"):
            modulefile = open(self.modulespath+ r"\foma_plugins.mod", 'r')
            modulelines = modulefile.readlines()
            modulefile.close()
            text=str(modulelines[0][2:]).decode('gbk') 
        else:
            text =None
        if os.path.basename(__file__).split('.')[0].split("_")[-1]!="update":
            self.win=QtGui.QMessageBox.about(self, u'温馨提示', u"已完成%s！！"%(text))
        else:
            self.win=QtGui.QMessageBox.about(self, u'温馨提示', u"MAYA通用配置本地版已同步完毕！！")

##本地文件json列表更新
if os.path.exists("C:/hq_tool/Maya/hq_tool_filelists.json")==False:
    invalidTypes =["db","inf","pyc"]
    cpanpath = r"C:/hq_tool/Maya"
    if os.path.exists(cpanpath)==False:
        mkcmd = 'mkdir "%s" '%(cpanpath.replace("/","\\"))
        subprocess.Popen(mkcmd,shell=True)
    if localize().walkDirs_CMD(cpanpath,0)!=None:
        filelists = [a for a in localize().walkDirs_CMD(cpanpath,0) if a.split(".")[-1] not in invalidTypes]
    else:
        filelists=[]
    dirlists=localize().walkDirs_CMD(cpanpath,1)
    filedirs = set([os.path.dirname(a) for a in filelists])
    puredirs = [a for a in list(set(dirlists)-filedirs) if os.listdir(a)==[] ]
    pathlists =  puredirs+filelists
    dd = json.dumps( pathlists, indent=4,encoding='GBK')
    file = open("C:/hq_tool/Maya/hq_tool_filelists.json", 'w')
    file.write(dd)
    file.close()


##本地化
if os.path.basename(__file__).split('.')[0].split("_")[-1]=="local":
    opanpath = mainpaths
    localpath = r"C:/hq_tool"
    localize().opan2local(opanpath, localpath,mainpaths+"/Maya","C:/hq_tool/Maya")
    earseCdirsCmd()

##拷贝module或者升级同步
if os.path.basename(__file__).split('.')[0].split("_")[-1]!="update":
    HQ_tool(). initsetup()
    HQ_tool(). updateVer(mainpaths+r"/programs/ToolManager/modules/"+os.path.basename(__file__).split('.')[0]+r".mod")
else:
    opanpath = mainpaths
    localpath = r"C:/hq_tool"
    localize().opan2local(opanpath, localpath,mainpaths+"/Maya","C:/hq_tool/Maya")
    earseCdirsCmd()

app = QtGui.QApplication(sys.argv)
window = finishbar()
#sys.exit()
