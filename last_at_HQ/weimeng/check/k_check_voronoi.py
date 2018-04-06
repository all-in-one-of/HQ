def k_check_voronoi():
    import maya.cmds as cc
    k_return=[]
    k_lsvos=cc.ls(type='unknownDag')
    for k_lsvo in k_lsvos:
        if 'voronoiNode' in k_lsvo:k_return.append(k_lsvo)
        
    return k_return          
        

    
