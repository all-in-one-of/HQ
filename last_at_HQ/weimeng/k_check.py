# coding=utf-8
def k_check(p,j,s):
    import json as ss
    import sys
    import maya.cmds as cc
    import maya.mel as mm
    import os    
    import time
    import datetime

    #j = 'E:/work/7_0314_wenti'
    o = 'D:/work/7_0314_wenti'
    op = 'D:/work/7_0314_wenti/other'


    #mongoDB的路径
    path='D:/ziliao/201707/python_site-packages'
    if not path in sys.path:
        sys.path.append(path)
    import datetime
    from bson.objectid import ObjectId
    import pymongo
    client=pymongo.MongoClient('10.99.40.10',27017)
    db = client['k_text']
    kpost = db['check']

    #maya后台检查脚本路径
    path2='D:/ziliao/201708/check'
    if not path in sys.path:
        sys.path.append(path2)
    sys.path.append(path2)



    import socket
    checkIP=('127.0.0.1',998)
    ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ksocket.connect(checkIP)
    sys.path.append('C:/Users/dengtao/Documents/maya/2015-x64/scripts') 
    reload(sys)
    sys.setdefaultencoding('gbk')       
    import fantaTexClass    
    k_envpath='E:/work/7_0327_mayapy/text5/release/json/' 
    k_enablefiles=ss.loads(open(r'%sk_enable.json' %k_envpath).read(),encoding='gbk')
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
            ksend={kprogres:kType}
            ksend=ss.dumps(ksend)
            ksocket.send(ksend)
            kreply=ksocket.recv(1024)
            #time.sleep(.1)


    #k_outputs=ss.dumps(k_Treturn)
    import k_checkVRmeshfiles27
    check_outsidefile=k_checkVRmeshfiles27.k_cachefinder()
    outsidefile=check_outsidefile.k_checkit()
    kNodedate = check_outsidefile.kNodedate

    import k_eOutsidePath2
    k_update = k_eOutsidePath2.k_editPath(j,o,op,outsidefile)

    mayaplugin_version=check_outsidefile.mayaplugin_version
    check_post={u"检查人":"k",u"上传时间":datetime.datetime.now(),"maya_check":k_Treturn,"Nodedate":kNodedate,"outsidefile":outsidefile,"k_update":k_update,u'插件版本':mayaplugin_version,u'工程目录':check_outsidefile.projectDir}
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





