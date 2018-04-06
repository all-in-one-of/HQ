def k_check_OpathCache():
    import maya.cmds as cc
    k_return=[]
    k_caches=cc.ls(type='cacheFile')
    for k_cache in k_caches:
        k_cp=cc.getAttr(k_cache+'.cachePath')
        if not 'o:' in k_cp and not 'O:' in k_cp:
            k_return.append(k_cache)
    return k_return                      