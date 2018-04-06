def k_check_Opathaisin():
    import maya.cmds as cc
    k_return=[]
    k_aiss=cc.ls(type='aiStandIn')

    for k_ais in k_aiss:
        k_aip=cc.getAttr(k_ais+'.dso')
        if k_aip:
            if not 'o:' in k_aip and not 'O:' in k_aip:
                    k_return.append(k_ais)
        else:k_return.append(k_ais)
    return k_return   