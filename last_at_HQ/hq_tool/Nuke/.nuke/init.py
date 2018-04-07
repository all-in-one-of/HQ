#coding=utf-8
import nuke
import os
import sys
import re
import platform


if platform.system() == "Windows":
    homepath = os.path.abspath('O:\hq_tool\Nuke\.nuke/')
elif platform.system() == "Linux":
    homepath = os.path.abspath('/Public/Ptd/Nuke/NukePlugin/')


targetDirs = [os.path.join(homepath, dirt) for dirt in os.listdir(homepath) if os.path.isdir(os.path.join(homepath, dirt))]

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
