def k003_check_History():
    import maya.cmds as cc
    k_return=[]
    deformers=["skinCluster","blendShape","ffd","wrap","cluster","nonLinear","sculpt","jiggle","wire","mesh","groupParts","groupId","nCloth","squamaNode","ropeNode","verNailNode","polyTransfer","polySmoothFace"]  
    k_deformerT=["skinCluster","blendShape","ffd","wrap","cluster","nonLinear","sculpt","jiggle","wire"]
    k_History1=cc.ls(type='mesh',ni=1)
    k_History2=cc.ls(type='nurbsSurface',ni=1)
    k_Historys=k_History1+k_History2
    for k_History in k_Historys:
        k_lhis=cc.listHistory(k_History)
        for k_lhi in k_lhis:
            if cc.nodeType(k_lhi) in k_deformerT:
                if cc.nodeType(k_History)=='mesh':
                    k_con=cc.listConnections((k_History+'.inMesh'),d=0,sh=1)
                if cc.nodeType(k_History)=='nurbsSurface':
                    k_con=cc.listConnections((k_History+'.create'),d=0,sh=1)
                if  k_con and not cc.nodeType(k_con[0]) in deformers and not 'shavedisplay' in k_History:
                    k_return.append(k_History)
                                
            
    return k_return












