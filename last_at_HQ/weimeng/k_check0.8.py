# coding=utf-8
def k_check(p,s):
    import json as ss
    import sys
    import maya.cmds as cc
    import os
    import socket
    import time
    checkIP=('127.0.0.1',998)
    ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ksocket.connect(checkIP)
    sys.path.append('\\\\ftdyproject\\digital\\film_project\\hq_tool\\Maya\\hq_maya\\scripts\\fantabox\\common') 
    reload(sys)
    sys.setdefaultencoding('gbk')       
    import check    
    k_envpath='E:/work/7_0327_mayapy/text2/release/json/' 
    k_enablefiles=ss.loads(open(r'%sk_enable.json' %k_envpath).read(),encoding='gbk')
    k_enables=ss.loads(s,encoding='gbk')       
    cc.file(p,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)
    k_Treturn={}

    k_enablesize=0
    for i in k_enables.keys():
        if k_enables[i][0]:
            k_enablesize+=1

    

    kpercent=100./k_enablesize
    kprogres=0
    for k_enable in k_enables:
        if k_enables[k_enable][0]:
            k_return='check.%s()' %k_enable
            k_returna=eval(k_return)
            k_update={k_enable:k_returna}
            k_Treturn.update(k_update)
            kprogres=kprogres+kpercent
            ksend={k_enable:(k_returna,kprogres)}
            ksend=ss.dumps(ksend)
            ksocket.send(ksend)
            kreply=ksocket.recv(1024)

    #k_outputs=ss.dumps(k_Treturn)
    ksocket.close()

    for k_Treturns in k_Treturn:
        if k_Treturn[k_Treturns]:
            print ('---------'+k_enablefiles[k_Treturns][2]+'--------------')
            for k_Treturnss in k_Treturn[k_Treturns]:
                print (k_Treturnss) 

