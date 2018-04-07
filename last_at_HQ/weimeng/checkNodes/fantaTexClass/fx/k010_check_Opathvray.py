def k010_check_Opathvray():
    import maya.cmds as cc
    k_return=[]
    if cc.pluginInfo('vrayformaya',q=1,loaded=1):
        k_vmeshs=cc.ls(type='VRayMesh')
        for k_vmesh in k_vmeshs:
            k_vm=cc.getAttr(k_vmesh+'.fileName')
            if not 'o:' in k_vm and not 'O:' in k_vm:
                k_return.append(k_vmesh)
    return k_return  
    