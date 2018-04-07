def k007_check_UNKNOWNREF():
    import maya.cmds as cc
    k_return=[]
    k_lsrefs=cc.ls(type='reference')
    for k_lsref in k_lsrefs:
        if '_UNKNOWN_REF_NODE_' in k_lsref:k_return.append(k_lsref)
    return k_return                  