import maya.cmds as cmds
def edo_exPolyWeights():
    path=''
    paths=cmds.fileDialog2(fileFilter='*.skw',dialogStyle=2)
    if paths:
        path=paths[0]
    if path=='':
        cmds.undoInfo(state=1)
        return False
    sels=cmds.ls(sl=1)
    coms=cmds.polyListComponentConversion(sels,tv=1)
    cmds.select(coms,r=1)
    cs=cmds.ls(sl=1,fl=1)
    if cs:
       fobj=open(path,'w')
    for c in cs:
        #c=cs[0]
        #cmds.select(c)
        infs=cmds.skinCluster(c,q=1,inf=1)
        sk=edo_findNodeFromHis(c,'skinCluster')
        ws=cmds.skinPercent(sk,c,q=1,v=1)
        l=len(infs)
        tx=c+':'
        for i in range(0,l):
            #i=0
            inf=infs[i]
            w=ws[i]
            if w==0.0:
                continue
            iw=inf+'='+str(w)
            tx=tx+iw+' '
        #print tx
        fobj.write(tx+'\n')
    fobj.close()
    
def edo_imPolyWeights():
    cmds.undoInfo(state=0)
    sels=cmds.ls(sl=1)
    path=''
    paths=cmds.fileDialog(dm='*.skw',m=0,t='import')
    if paths:
        path=paths
    if path=='':
        cmds.undoInfo(state=1)
        return False
    fobj=open(path,'r')
    tx=[]
    for line in fobj.readlines():
        tx.append(line)
    fobj.close()
    lc=len(tx)
    n=0
    for t in tx:
        #t=tx[0]
        if n%1000==0:
            print str(n)+'/'+str(lc)
        n=n+1
        t=t.replace('\n','')
        sp=t.split(':')
        c=sp[0]
        obj=c.split('.')[0]
        if (not obj in sels) and (not sels==[]):
            continue
        iw=sp[1]
        iws=iw.split(' ')
        sk=edo_findNodeFromHis(c,'skinCluster')
        edo_setVertexWeightZero(sk,c)
        tvs=edo_combineTheWeightData(iws)
        tvsl=[]
        lst=tvs.keys()
        for l in lst:
            #l=lst[0]
            tvsl.append((l,tvs[l]))
        #print tvsl
        #edo_lockAllInfluence(sk)
        cmds.skinPercent(sk,c,tv=tvsl)
        cmds.skinCluster(sk,e=1,nw=1)
    cmds.undoInfo(state=1)

def edo_lockAllInfluence(sk):
    cmds.skinCluster(sk,e=1,nw=1)
    infs=cmds.skinCluster(sk,q=1,inf=1)
    for i in infs:
        cmds.setAttr(i+'.lockInfluenceWeights',0)

def edo_combineTheWeightData(iws):
    tvs={}
    #iws=['head_jnt=0.5','head_jnt=0.6','joint1=0.2']
    for i in iws:
        #i=iws[2]
        if i=='\r' or i=='':
            continue
        else:
            isp=i.split('=')
            inf=isp[0]
            w=float(isp[1])
            if not inf in tvs.keys():
                tvs[inf]=w
            else:
                tvs[inf]=tvs[inf]+w
    return tvs

def edo_setVertexWeightZero(sk,c):
    cmds.skinCluster(sk,e=1,nw=0)
    infs=cmds.skinCluster(sk,q=1,inf=1)
    tvs=[]
    for i in infs:
        #i=infs[0]
        tvs.append((i,0))
    #print tvs
    cmds.skinPercent(sk,c,tv=tvs)
    
#edo_findNodeFromHis(name,type)
def edo_findNodeFromHis(name,type):
    #name='twodline_curve'
    #type='tweak'
    node=''
    hiss=cmds.listHistory(name)
    for his in hiss:
        if cmds.nodeType(his)==type:
            node=his
    return node
    
#edo_modifySkinWeightData('F:/aaa.skw','F:/SKINtemplate_GDCRIG_to_HUMANIK.skt')  
def edo_modifySkinWeightData(data='',temp=''):
    if data=='' or temp=='':
        return False
    #data='F:/skinWeight.skw'
    #temp='F:/SKINtemplate_GDCRIG_to_HUMANIK.skt'
    dobj=open(data,'r')
    dtx=dobj.readlines()
    dobj.close()
    tobj=open(temp,'r')
    ttx=tobj.readlines()
    tobj.close()
    ndtx=[]
    for dt in dtx:
        #dt=dtx[0]
        #print dt
        for tt in ttx:
            #tt=ttx[0]
            ttr=tt
            while (ttr[-1]=='\n') or (ttr[-1]=='\r'):
                ttr=ttr[:-1]
            #print ttr
            sp=ttr.split(' ')
            rps=sp[0].split(':')
            rd=sp[1]
            for rp in rps:
                #rp=rps[0]
                dt=dt.replace(rp,rd)
        ndtx.append(dt)
        print dt
    nobj=open(data,'w')
    for ndt in ndtx:
        #ndt=ndtx[0]
        nobj.write(ndt)
    nobj.close()