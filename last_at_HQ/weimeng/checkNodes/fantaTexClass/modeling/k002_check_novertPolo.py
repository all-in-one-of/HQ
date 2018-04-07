def k002_check_novertPolo():
    k_novertPolo=[]
    import maya.cmds as cc
    k_lsms = cc.ls(type='mesh')  
    for k_lsm in k_lsms:
        k_vr = cc.polyEvaluate(k_lsm, v=1)
        if not 'shave' in k_lsm and not k_vr:
            k_novertPolo.append(k_lsm)

    return k_novertPolo