#coding=cp936
#coding=utf-8
from pymel import versions
import sys
import os
def pySource(filePath):
    myFile = os.path.basename(filePath)
    dir = os.path.dirname(filePath)
    fileName = os.path.splitext(myFile)[0]
    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
            if not pathfound:
                sys.path.append( dir )
        exec('import ' +fileName) in globals()
        exec( 'reload( ' + fileName + ' )' ) in globals()
    return fileName
ver =  versions.current()
if str(ver) =="201300":
    pySource( '//10.99.1.12/数码电影/临时交换/02生产二线/02G角色/员工文件/X_徐思健/python_source/python_source_2013/SJMtoolbox_2013.pyc')
    print "This is SJtoolbox of Maya2013Version,enjoy it"
if str(ver) =="201516":
    pySource( '//10.99.1.12/数码电影/临时交换/02生产二线/02G角色/员工文件/X_徐思健/python_source/python_source_2015/SJMtoolbox_2015.pyc')
    print "This is SJtoolbox of Maya2015Version,enjoy it"