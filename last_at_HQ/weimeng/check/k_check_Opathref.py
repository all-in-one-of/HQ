def k_check_Opathref():
    import maya.cmds as cc
    k_return=[]
    k_refs=cc.file(q=1,r=1)
    for k_ref in k_refs:
        if not 'o:' in k_ref and not 'O:' in k_ref:
            k_return.append(k_ref)
    return k_return
    
    
    
