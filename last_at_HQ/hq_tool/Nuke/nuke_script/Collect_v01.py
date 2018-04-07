from shutil import copy
import os

def Collect():
    p=nuke.Panel('Collect')
    p.addEnumerationPulldown('choose','all single')
    p.addFilenameSearch('path','')
    k=p.show()
    a=nuke.allNodes('Read')
    outpath=p.value('path')
    list=[]

    if k==1:
        def sName(self,num):
            num='%04d' % num
            if '####' in self:  
                return self.replace('####',num)
            if '%04d' in self:
                return self.replace('%04d',num)
        
        rootName=os.path.basename(nuke.root()['name'].value())
        foot=rootName.split('.')[0]+'/'
        scriptpath=outpath+foot+rootName
        savepath=outpath+foot
#打包所有素材
        if p.value('choose')=='all':
            for i in a:
                rname=i.name()
                if not rname in list:
                    Fframe=i['first'].value()
                    Lframe=i['last'].value()
                    cc=i['file'].value()
                    rootpath=unicode(cc,'utf8')
                    name=rootpath.split('/')
                    copypath=savepath+name[-2]+'/'
                    finpath=copypath+name[-1]
                    if i.clones()!=0:
                        list.append(rname)
                    if not os.path.exists(copypath) :
                        os.makedirs(copypath)
                    for v in range(Fframe,Lframe+1):
                        if Fframe==Lframe:
                            copy(rootpath,finpath)
                            finpath=finpath.encode('utf8')
                            i['file'].setValue(finpath)
                        else:
                            input=sName(rootpath,v)
                            output=sName(finpath,v)
                            if os.path.exists(input):
                                copy(input,output)
                            i['file'].setValue(finpath)
                else:
                    pass
                
            nuke.scriptSaveAs(scriptpath)
#打包单帧素材            
        if p.value('choose')=='single':
            for i in a:
                rname=i.name()

                if not rname in list:
                    Fframe=i['first'].value()
                    Lframe=i['last'].value()                
                    frame=nuke.frame()
                    cc=i['file'].value()
                    rootpath=unicode(cc,'utf8')
                    name=rootpath.split('/')
                    copypath=savepath+name[-2]+'/'
                    finpath=copypath+name[-1]
                    if i.clones()!=0:
                        list.append(rname)
                    if not os.path.exists(copypath) :
                        os.makedirs(copypath)
                    
                    if Fframe==Lframe:
                        copy(rootpath,finpath)
                        finpath=finpath.encode('utf8')
                        i['file'].setValue(finpath)
                    else:
                        input=sName(rootpath,frame)
                        output=sName(finpath,frame)

                        if os.path.isfile(input):
                            
                            copy(input,output)
                            output=output.encode('utf8')
                            i['file'].setValue(output)
                else:
                    pass
            nuke.scriptSaveAs(scriptpath)
    else:
        pass
