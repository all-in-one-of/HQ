def k_check_Opathtex():
    import maya.cmds as cc
    k_return=[]
    k_fpaths=cc.ls(type='file')
    for k_fpath in k_fpaths:
        k_fp=cc.getAttr(k_fpath+'.fileTextureName')
        if not 'o:' in k_fp and not 'O:' in k_fp:
            k_return.append(k_fpath)
    return k_return                      