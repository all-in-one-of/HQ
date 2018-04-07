def k015_check_displink():
    import maya.cmds as cc
    k_return=[]
    k_lsdiss=cc.ls(type='displacementShader')
    for k_lsdis in k_lsdiss:
        k_listdis=cc.listConnections(k_lsdis,type='shadingEngine',d=1)
        if k_listdis:pass
        else:k_return.append(k_lsdis)
        
    return k_return          
        

    
