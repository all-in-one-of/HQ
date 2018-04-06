def k_check_lostTexture():
    import maya.cmds as cc
    import os
    import maya.app.general.fileTexturePathResolver as zz
    k_return=[]
    k_selfiles=cc.ls(type='file')
    for k_selfile in k_selfiles:
        k_filepath=cc.getAttr(k_selfile+'.fileTextureName')
        k_existf=os.path.exists(k_filepath)
        k_uvmode=cc.getAttr(k_selfile+'.uvTilingMode')  
        if k_existf and k_uvmode==3:
            k_getUDIMp=zz.getFilePatternString(k_filepath, False, 3)
            k_exudim=zz.findAllFilesForPattern(k_getUDIMp,None)
            if not k_exudim:
                k_return.append(k_selfile) 
        elif not k_existf:
            k_return.append(k_selfile) 
    return k_return                        