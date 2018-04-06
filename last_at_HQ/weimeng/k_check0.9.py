# coding=utf-8
def k_check(p,s):
    import json as ss
    import sys
    import maya.cmds as cc
    import os
    sys.path.append('E:\\work\\7_0327_mayapy\\k_moni') 
    reload(sys)
    sys.setdefaultencoding('gbk')       
    import k_py    
    k_envpath='E:/work/7_0327_mayapy/text2/release/json/'  
    #k_loadpath=ss.loads(open(r'%sk_path.json' %k_envpath).read(),encoding='gbk') 
    k_enablefiles=ss.loads(open(r'%sk_enable.json' %k_envpath).read(),encoding='gbk')
    k_enables=ss.loads(s,encoding='gbk')       
    cc.file(p,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)    
    k_Treturn={}
    for k_enable in k_enables:
        if k_enables[k_enable][0]:            
            k_return='k_py.%s()' %k_enable
            k_returna=eval(k_return)
            k_update={k_enable:k_returna}
            k_Treturn.update(k_update)                    
    k_outputs=ss.dumps(k_Treturn)
    for k_Treturns in k_Treturn:

        if k_Treturn[k_Treturns]:
            k_exp=open(k_envpath+'k_return.txt','a')
            #print ('---------'+k_enablefiles[k_Treturns][2]+'  ≤‚ ‘--------------')
            k_exp.writelines('---------'+k_enablefiles[k_Treturns][2]+'  ≤‚ ‘--------------')
            for k_Treturnss in k_Treturn[k_Treturns]:
                #print k_Treturnss
                k_exp.writelines(k_Treturnss)
            k_exp.close()
    

