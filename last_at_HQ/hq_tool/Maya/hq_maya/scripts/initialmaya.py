
import sys
import ctypes.wintypes
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
hostname = buf.value
arnoldpath = []
modulespath= hostname+"\maya\modules"
modulefile = open(modulespath+ r"\foma_plugins.mod", 'r')
modulelines = modulefile.readlines()
modulefile.close()
for moduleline in modulelines:
    if moduleline.find("+ MAYAVERSION:2015 mtoa")!=-1:
        try:
            Arnoldname = moduleline[moduleline.find("Arnold_"):][:-10]
        except:
            Arnoldname=[]
        if Arnoldname!=[]:
            arnoldpath.append(r"O:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
if arnoldpath[0] not in sys.path:
    sys.path.append(arnoldpath[0])
import maya.standalone
maya.standalone.initialize(name="python")
import pymel.core
if pymel.core.pluginInfo("pgYetiMaya",q=1,loaded=1,name=1)==0:
    try:
        pymel.core.loadPlugin("pgYetiMaya")
    except:
        print "failed to load pgYetiMaya",
if pymel.core.pluginInfo("mtoa",q=1,loaded=1,name=1)==0:
    try:
        pymel.core.loadPlugin("mtoa")
    except:
        print "failed to load mtoa",
