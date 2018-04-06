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
            if k_enable=='k_check_novertPolo':
                k_returna=k_py.k_check_novertPolo.k_check_novertPolo()
                k_update={'k_check_novertPolo':k_returna}
                k_Treturn.update(k_update)
                
            elif k_enable=='k_check_hairlinkarnold':
                k_returna=k_py.k_check_hairlinkarnold.k_check_hairlinkarnold()
                k_update={'k_check_hairlinkarnold':k_returna}
                k_Treturn.update(k_update)
    
            elif k_enable=='k_check_History':
                k_returna=k_py.k_check_History.k_check_History()
                k_update={'k_check_History':k_returna}
                k_Treturn.update(k_update)            
    
            elif k_enable=='k_check_vshapeNode':
                k_returna=k_py.k_check_vshapeNode.k_check_vshapeNode()
                k_update={'k_check_vshapeNode':k_returna}
                k_Treturn.update(k_update)   
    
            elif k_enable=='k_check_wkHeadsUp':
                k_returna=k_py.k_check_wkHeadsUp.k_check_wkHeadsUp()
                k_update={'k_check_wkHeadsUp':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_voronoi':
                k_returna=k_py.k_check_voronoi.k_check_voronoi()
                k_update={'k_check_voronoi':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_UNKNOWNREF':
                k_returna=k_py.k_check_UNKNOWNREF.k_check_UNKNOWNREF()
                k_update={'k_check_UNKNOWNREF':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_unknown':
                k_returna=k_py.k_check_unknown.k_check_unknown()
                k_update={'k_check_unknown':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_sharedRef':
                k_returna=k_py.k_check_sharedRef.k_check_sharedRef()
                k_update={'k_check_sharedRef':k_returna}
                k_Treturn.update(k_update)  
                
            elif k_enable=='k_check_Opathvray':
                k_returna=k_py.k_check_Opathvray.k_check_Opathvray()
                k_update={'k_check_Opathvray':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_Opathref':
                k_returna=k_py.k_check_Opathref.k_check_Opathref()
                k_update={'k_check_Opathref':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_OpathCache':
                k_returna=k_py.k_check_OpathCache.k_check_OpathCache()
                k_update={'k_check_OpathCache':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_Opathaisin':
                k_returna=k_py.k_check_Opathaisin.k_check_Opathaisin()
                k_update={'k_check_Opathaisin':k_returna}
                k_Treturn.update(k_update)              
                            
            elif k_enable=='k_check_Opathabc':
                k_returna=k_py.k_check_Opathabc.k_check_Opathabc()
                k_update={'k_check_Opathabc':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_displink':
                k_returna=k_py.k_check_displink.k_check_displink()
                k_update={'k_check_displink':k_returna}
                k_Treturn.update(k_update)  
    
            elif k_enable=='k_check_uuoig':
                k_returna=k_py.k_check_uuoig.k_check_uuoig()
                k_update={'k_check_uuoig':k_returna}
                k_Treturn.update(k_update)            
                
                
    k_output=ss.dumps(k_Treturn)
    
    
    k_outpath=open('%sk_output.json' %k_envpath,'w')
    k_outpath.writelines(k_output)
    k_outpath.close()


