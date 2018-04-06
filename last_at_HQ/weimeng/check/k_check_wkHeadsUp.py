def k_check_wkHeadsUp():
    import maya.cmds as cc
    k_return=[]
    k_wkHeads=cc.ls(type='expression')
    for k_wkHead in k_wkHeads:
        if 'wkHeadsUp' in k_wkHead:k_return.append(k_wkHead)
    return k_return