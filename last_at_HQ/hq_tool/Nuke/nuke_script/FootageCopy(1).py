import os,shutil,time,threading,nuke,math

def FootageCopy():
    a=[i for i in nuke.allNodes() if ''.join(x for x in i.name() if x.isalpha()) == 'Camera' or ''.join(x for x in i.name() if x.isalpha()) == 'Read' or ''.join(x for x in i.name() if x.isalpha()) == 'ReadGeo' or ''.join(x for x in i.name() if x.isalpha()) == 'Axis']
    
    num=100.0/len(a)
    t=0
    readlist=[]
    task = nuke.ProgressTask("Moving")            
    mm = nuke.root()['name'].value().split('/')
    cc = mm[0]+'/'+mm[1]+'/'+mm[2]+'/'+mm[3]
    scrpath = cc+'/'+'Footage_Final'
    
    
    for i in a:
    
        if task.isCancelled():
            break
        file=i['file'].value()
        if file != '':
            readname=i.name()       
            filename=i['file'].value()
            dirname=os.path.dirname(filename)
            pathlist=dirname.split('/')
            b=os.listdir(dirname)
            if not readname in readlist:
                if pathlist[0]=='T:'or pathlist[0]=='S:':
                
                    if 'footage' in dirname or 'Footage' in dirname:
    
        
                        if 'Footage' in dirname:
                            copypath=os.path.dirname(dirname.replace('Footage','Footage_Final'))                      
    
                        else:
                            copypath=os.path.dirname(dirname.replace('footage','Footage_Final'))
    
                        dirname=unicode(dirname,'utf8')
                        copypath=unicode(copypath,'utf8')
    
                        if not os.path.exists(copypath) :
                            os.makedirs(copypath)   
                        if os.path.exists(dirname):
                            try:
            
                                shutil.move(dirname,copypath)
        
                            except shutil.Error:
                                footpath=copypath+'/'+dirname.split('/')[-1]
                                newpath=copypath+'/'+'temp'
                                frompath=newpath+'/'+dirname.split('/')[-1]
                                shutil.move(footpath,newpath)
                                shutil.move(dirname,copypath)
                                newlist=os.listdir(frompath)
                                if not os.path.exists(newpath) :        
                                    os.makedirs(newpath)
    
                                for v in newlist:
                                    topath=frompath+'/'+v
                                    shutil.move(topath,footpath)    
    
        t=t+num
        setT=int(math.floor(t))
        task.setMessage("%s" % filename)
        task.setProgress(setT)      
        time.sleep(0.1)
        readlist.append(readname)



def run():

    threading.Thread(None,FootageCopy).start()



