import sys
import ctypes.wintypes
import os

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
hostname = buf.value
arnoldpath = []
modulespath= hostname+"\maya\modules"

if os.path.exists(modulespath+ r"\foma_plugins.mod"):
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
                arnoldpath.append(r"//10.99.1.13/hq_tool/Maya/Arnold/"+Arnoldname+r"_Maya2015/scripts")
                
elif os.path.exists(r'C:/solidangle/mtoadeploy/2015/scripts'):
    arnoldpath.append(r'C:/solidangle/mtoadeploy/2015/scripts')
    
if arnoldpath :                              
    if arnoldpath[0] not in sys.path:
        sys.path.append(arnoldpath[0])
        
import maya.standalone
maya.standalone.initialize(name="python")








