def k001_check_hairlinkarnold():
    import maya.cmds as cc
    k_return=[]
    k_lsshaveHair=[]
    k_lshairSystem=[]
    if cc.pluginInfo('shaveNode',q=1,loaded=1):
        k_lsshaveHair=cc.ls(type='shaveHair')
        k_lshairSystem=cc.ls(type='hairSystem')
    for k_shave in k_lsshaveHair:
        k_attrn=[]
        try:
            k_attrn=cc.connectionInfo((k_shave+".aiHairShader"),id=1)       
        except:
            pass
        if k_attrn:
            k_listai=cc.listConnections(k_shave+".aiHairShader",d=1,type="aiHair")
            k_listal=cc.listConnections(k_shave+".aiHairShader",d=1,type="alHair")
            if k_listai or k_listal:pass
            else :k_return.append(k_shave)
        else:k_return.append(k_shave)
        
    return k_return          
        
if __name__=='__main__':
    k_check_hairlinkarnold()
    
    
