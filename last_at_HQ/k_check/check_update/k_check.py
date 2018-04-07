# coding=utf-8
def k_check(p,j,o,s):
    import json as ss
    import sys
    import maya.cmds as cc
    import maya.mel as mm
    import os    
    import time
    import datetime

    k_fantabox  = 'O:/hq_tool/Maya/hq_maya/scripts'
    k_json      = k_fantabox+'/fantabox'
    k_python_sp = 'O:/hq_tool/programs/python_site-packages'
    #k_python_mod= u'//10.99.1.12/数码电影/临时交换/08技术/个人文件夹/L练月标/HqFtp/release/init'

    #j = 'E:/work/7_0314_wenti'
    #o = 'D:/work/7_0314_wenti'
    op = o+'/ftbox_otherfile'


    #mongoDB的路径
    #path='D:/ziliao/201707/python_site-packages'
    if not k_python_sp in sys.path:
        sys.path.append(k_python_sp)
    import datetime
    from bson.objectid import ObjectId
    import pymongo
    client=pymongo.MongoClient('10.99.40.10',27017)
    db = client['k_text']
    kpost = db['check']

    #maya后台检查脚本路径
    #path2='D:/ziliao/201708/check'
    #if not k_python_mod in sys.path:
        #sys.path.append(k_python_mod)



    import socket
    checkIP=('127.0.0.1',998)
    ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ksocket.connect(checkIP)

    #插件模块地址
    #sys.path.append('C:/Users/dengtao/Documents/maya/2015-x64/scripts') 
    if not k_fantabox in sys.path:
        sys.path.append(k_fantabox)

    reload(sys)
    sys.setdefaultencoding('gbk')       
    import fantabox   

    #json文件地址
    #k_envpath='E:/work/7_0327_mayapy/text5/release/json/' 
    k_enablefiles=ss.loads(open(r'%sFantaBox_mayacheck.json' %k_json).read(),encoding='gbk')
    k_enables=ss.loads(s,encoding='gbk')       
    cc.file(p,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)

    
    mm.eval('setProject "%s";'%j) 

    
    k_Treturn={}

    module={'modeling':'mod','rendering':'ren','fx':'fx','common':'com','animation':'ani','rigging':'rig'}
    
    k_enablesize=0
    for i in k_enables.keys():
        if k_enables[i][0]:
            k_enablesize+=1

    kpercent=100./k_enablesize
    kprogres=0
    for k_enable in k_enables:
        if k_enables[k_enable][0]:
            kType=1

            kmod=k_enablefiles[k_enable][3]
            print kmod
            new_k_enable=(module[kmod]+'.'+k_enable)
            print new_k_enable
            print 'fantaTexClass.%s()' %new_k_enable
            k_return='fantaTexClass.%s()' %new_k_enable
            k_returna=eval(k_return)
            if k_returna:
                kType=2
            #k_update={k_enable:k_returna}
            k_update={k_enablefiles[k_enable][2]:k_returna}
            k_Treturn.update(k_update)

            kprogres=kprogres+kpercent
            if kprogres >= 99.9:
                kprogres=100
            ksend={kprogres:kType}
            ksend=ss.dumps(ksend)
            ksocket.send(ksend)
            kreply=ksocket.recv(1024)
            #time.sleep(.1)


    #k_outputs=ss.dumps(k_Treturn)
    import k_checkOutSideFile
    check_outsidefile=k_checkOutSideFile.k_cachefinder()
    outsidefile=check_outsidefile.k_checkit()
    kNodedate = check_outsidefile.kNodedate

    import k_editOutsidePath

    k_updata = k_editOutsidePath.k_editPath(j,o,outsidefile)
    k_updata.k_checkPath()
    k_pathUpdate = k_updata.kupdate



    mayaplugin_version=check_outsidefile.mayaplugin_version
    check_post={u"检查人":"k",u"上传时间":datetime.datetime.now(),"maya_check":k_Treturn,"Nodedate":kNodedate,"outsidefile":outsidefile,"update":k_pathUpdate,u'插件版本':mayaplugin_version,u'工程目录':check_outsidefile.projectDir}
    kpost_id=kpost.insert(check_post)
    #print kpost_id
    ksend={"_id":str(kpost_id)}
    ksend=ss.dumps(ksend)
    ksocket.send(ksend)
    ksocket.close()



'''    for k_Treturns in k_Treturn:
        if k_Treturn[k_Treturns]:
            print ('---------'+k_enablefiles[k_Treturns][2]+'--------------')
            for k_Treturnss in k_Treturn[k_Treturns]:
                print (k_Treturnss) '''





