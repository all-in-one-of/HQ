def k_check_vshapeNode():
    import maya.cmds as cc
    import re
    k_return=[]
    k_lsmeshs=cc.ls(type='mesh')
    k_kmeshs=[]
    k_kNurbs=[]
    k_kCurvs=[]
    for k_lsmesh in k_lsmeshs:
        if not cc.getAttr(k_lsmesh+'.intermediateObject'):
            k_kmeshs.append(k_lsmesh)
    k_lsNurbs=cc.ls(type='nurbsSurface')
    for k_lsNurb in k_lsNurbs:
        if not cc.getAttr(k_lsNurb+'.intermediateObject'):
            k_kNurbs.append(k_lsNurb)    
    #k_lsCurvs=cc.ls(type='nurbsCurve')
    #for k_lsCurv in k_lsCurvs:
        #if not cc.getAttr(k_lsCurv+'.intermediateObject'):
            #k_kCurvs.append(k_lsCurv)      
    k_lsalls=k_kmeshs+k_kNurbs
    for k_lsall in k_lsalls:

        
        if '|' in k_lsall:
            k_lsshorts=k_lsall.split('|')
            k_lsshort=k_lsshorts[-1]         
            k_lsT=cc.listRelatives(k_lsall,p=1,type='transform')
            k_qdlsm=re.sub(r'\d+$', "", k_lsshort)
            k_qdlst=re.sub(r'\d+$', "", k_lsT[0])            
            k_qdmg=[]
            k_qdtg=[]
            k_qdm=re.search(r'\d+$',k_lsshort)
            if k_qdm:k_qdmg=k_qdm.group()        
            k_qdt=re.search(r'\d+$',k_lsT[0])
            if k_qdt:k_qdtg=k_qdt.group()
                    

            
            if not k_lsT[0]+'Shape'==k_lsshort and not k_qdlst+'Shape'==k_qdlsm :
                k_return.append(k_lsall)

            if  k_qdlst+'Shape'==k_qdlsm:
                if k_qdmg and k_qdtg and not k_qdmg==k_qdtg:
                    k_return.append(k_lsall)

                    
        else :    
            k_lsT=cc.listRelatives(k_lsall,p=1,type='transform')
            k_qdlsm=re.sub(r'\d+$', "", k_lsall)
            k_qdlst=re.sub(r'\d+$', "", k_lsT[0])
            k_qdm=re.search(r'\d+$',k_lsall)
            k_qdmg=[]
            k_qdtg=[]
            if k_qdm:k_qdmg=k_qdm.group()        
            k_qdt=re.search(r'\d+$',k_lsT[0])
            if k_qdt:k_qdtg=k_qdt.group()        
                
            if not k_lsT[0]+'Shape'==k_lsall and not k_qdlst+'Shape'==k_qdlsm :
                k_return.append(k_lsall)
            if  k_qdlst+'Shape'==k_qdlsm:
                if k_qdmg and k_qdtg and not k_qdmg==k_qdtg:
                    k_return.append(k_lsall)
                                            
                
    return k_return

if __name__=='__main__':
    k_check_vshapeNode()






