def k016_check_uuoig():
    import maya.cmds as cc
    k_return=[]
    k_uuoigs1=cc.ls(type='mesh',io=1)
    k_uuoigs2=cc.ls(type='nurbsSurface',io=1)
    k_uuoigs=k_uuoigs1+k_uuoigs2
    for k_uuoig in k_uuoigs:
        k_co=cc.listConnections(k_uuoig,s=0)
        if not k_co:k_return.append(k_uuoig)
    return k_return
    
    
