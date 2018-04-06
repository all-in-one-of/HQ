# coding=utf-8
def k_check():
    import json as ss
    import sys
    import maya.cmds as cc
    import os
    sys.path.append('E:\\work\\7_0327_mayapy\\k_moni')        
    import k_py    
    k_envpath='E:/work/7_0327_mayapy/k_moni/'  
    k_loadpath=ss.loads(open(r'%sk_path.json' %k_envpath).read(),encoding='gbk') 
    k_enables=ss.loads(open(r'%sk_enable.json' %k_envpath).read(),encoding='gbk')   
    cc.file(k_loadpath,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)    
    k_Treturn={}
    for k_enable in k_enables:
        if k_enables[k_enable][0]:
            k_return='k_py.%s.%s()' %(k_enable,k_enable)
            k_returna=eval(k_return)
            k_update={k_enable:k_returna}
            k_Treturn.update(k_update)                    
    k_output=ss.dumps(k_Treturn)   
    k_outpath=open('%sk_output.json' %k_envpath,'w')
    k_outpath.writelines(k_output)
    k_outpath.close()
