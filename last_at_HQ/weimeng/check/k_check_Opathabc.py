def k_check_Opathabc():
    import maya.cmds as cc
    k_return=[]
    k_abcs=cc.ls(type='AlembicNode')
    for k_abc in k_abcs:
        k_ab=cc.getAttr(k_abc+'.abc_File')
        if not 'o:' in k_ab and not 'O:' in k_ab:
            k_return.append(k_abc)
    return k_return                      