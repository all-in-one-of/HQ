def k009_check_sharedRef():
    import maya.cmds as cc
    k_return=[]
    k_shaverefs=cc.ls(type='reference')
    for k_shaveref in k_shaverefs:
        if 'sharedReferenceNode' in k_shaveref:k_return.append(k_shaveref)
    return k_return