import nuke
import os
import sys
import re


if platform.system() == "Windows":
    homepath = os.path.abspath('D:/NukePlugin/')
elif platform.system() == "Linux":
    homepath = os.path.abspath('/Public/Ptd/Nuke/NukePlugin/')


nukePattern = re.compile('nuke_([a-z]+)$')
sysPattern = re.compile('sys_([a-z]+)$')

for i in targetDirs:
    thisDir = os.path.split(i)[1]
    if nukePattern.match(thisDir):
        nuke.pluginAddPath(i)
    if sysPattern.match(thisDir):
        sys.path.append(i)

if not nuke.GUI:
    nuke.tprint('\n\n')
    for i in nuke.pluginPath():
        nuke.tprint(i)
    nuke.tprint('\n\n')
    for i in sys.path:
        nuke.tprint(i)
    nuke.tprint('\n\n')

def createWriteDir(): 
    import nuke, os 
    file = nuke.filename(nuke.thisNode()) 
    dir = os.path.dirname( file ) 
    osdir = nuke.callbacks.filenameFilter( dir ) 
    try: 
        os.makedirs( osdir ) 
        return 
    except: 
        return  
nuke.addBeforeRender( createWriteDir )