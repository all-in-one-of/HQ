#coding:utf-8
__author__ = 'Xusijian'
__date__    = '2017-04-12'
import os
import ctypes.wintypes
import shutil
from PySide import  QtGui

class HQ_tool():
    def __init__(self):
        self.CSIDL_PERSONAL= 5       # My Documents
        self.SHGFP_TYPE_CURRENT= 0   # Want current, not default value
        self.buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, self.CSIDL_PERSONAL, 0, self.SHGFP_TYPE_CURRENT, self.buf)
        self.hostname = self.buf.value
        self.modulespath= self.hostname+"\maya\modules"
        self.mayaver = [r"\maya\2015-x64",r"\maya\2013-x64"]
        self.rendererDesc = [r"O:\hq_tool\Maya\Arnold\Arnold_1.2.3.1_Maya2015\arnoldRenderer.xml",r"O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\vrRenderer.xml"]
    def updateVer(self,path):
        if os.path.exists(self.modulespath):
            if os.path.exists(self.modulespath+r"\foma_plugins.mod"):
                os.remove(self.modulespath+r"\foma_plugins.mod")
                shutil.copyfile(path,self.modulespath+r"\foma_plugins.mod")
            else:
                shutil.copyfile(path, self.modulespath + r"\foma_plugins.mod")
        else:
            os.mkdir(self.modulespath)
            if os.path.exists(self.modulespath+r"\foma_plugins.mod"):
                os.remove(self.modulespath+r"\foma_plugins.mod")
                shutil.copyfile(path,self.modulespath+r"\foma_plugins.mod")
            else:
                shutil.copyfile(path, self.modulespath + r"\foma_plugins.mod")
    def initsetup(self):
        dirlist = []
        modulesdirs = [self.hostname+r"\maya\modules",self.hostname+r"\maya\2015-x64\modules",r"C:\Program Files\Autodesk\Maya2015\modules",self.hostname+r"\maya\2013-x64\modules",r"C:\Program Files\Autodesk\Maya2013\modules"]
        tarlist =["mtoa.mod","pgYetiMaya.mod","VRayForMaya.module","shaveHaircut"]
        for modulesdir in modulesdirs:
            if os.path.exists(modulesdir):
                dirlistpath  = [modulesdir+"\\"+i for i in os.listdir(modulesdir) if  i  in tarlist]
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
            if os.path.exists(r"C:\\Program Files\\Autodesk\\Maya2015\\bin\\rendererDesc\\"+os.path.basename(rendererDesc)):
                os.remove(r"C:\\Program Files\\Autodesk\\Maya2015\\bin\\rendererDesc\\"+os.path.basename(rendererDesc))
                shutil.copyfile(rendererDesc, r"C:\\Program Files\\Autodesk\\Maya2015\\bin\\rendererDesc\\"+os.path.basename(rendererDesc))
            else:
                if os.path.exists(r"C:\Program Files\Autodesk\Maya2015\bin\rendererDesc"):
                    shutil.copyfile(rendererDesc,r"C:\\Program Files\\Autodesk\\Maya2015\\bin\\rendererDesc\\"+os.path.basename(rendererDesc))
                else:
                    print "maya2015 error installed!!",

        for mayavers in self.mayaver:
            if os.path.exists( self.hostname+mayavers):
                if os.path.exists( self.hostname+mayavers+r"\maya.env"):
                    oldenv = open(self.hostname +mayavers+r"\maya.env", 'r')
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
                            if os.path.exists( self.hostname+mayavers+r"\maya_bak.env"):
                                os.remove(self.hostname+mayavers+r"\maya_bak.env")
                            shutil.copyfile(self.hostname + mayavers+r"\maya.env",self.hostname + mayavers+r"\maya_bak.env")
                            file = open(self.hostname+mayavers+r"\maya.env", 'w')
                            blank = ""
                            file.write(blank)
                            file.close()
                        else:
                            pass
                    else:
                        pass
                else:
                    file = open(self.hostname+mayavers+r"\maya.env", 'w')
                    blank = ""
                    file.write(blank)
                    file.close()
            else:
                pass
            if os.path.exists(r"C:\Program Files\Autodesk\Maya2015\bin\Cg\shaveHair.cgfx")==False:
                shutil.copyfile(r"O:\hq_tool\Maya\Shave\shave_1.1_maya2015\bin\Cg\shaveHair.cgfx",r"C:\Program Files\Autodesk\Maya2015\bin\Cg\shaveHair.cgfx")
            else:
                pass

class finishbar(QtGui.QWidget):
    def __init__(self):
        super(finishbar, self).__init__()
        self.initUI()
    def initUI(self):
        self.win=QtGui.QMessageBox.about(self, u'Famo configure', u"MAYA2015吴哥配置已完成！！    ")
HQ_tool(). initsetup()
HQ_tool(). updateVer(r"O:\hq_tool\famo_configure\modules\famo_configure_wuge.mod")
import sys
app = QtGui.QApplication(sys.argv)
window = finishbar()
#sys.exit(app.exec_())
