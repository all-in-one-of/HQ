def k_check_unknown():
    import maya.cmds as cc
    k_return=[]
    k_unknowns=cc.ls(type='unknown')
    k_return=k_unknowns
    return k_return