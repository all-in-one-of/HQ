import edo_batchWindowDesign
import sys
import PyQt4
import PyQt4.QtGui as QtGui,PyQt4.QtCore as QtCore
import os
import compiler
import shutil

qtpath=str(PyQt4.__file__).replace('__init__.pyc','')


class edo_batchWindow(edo_batchWindowDesign.Ui_edo_batchWindow):
    def setupUi(self, edo_batchWindow):
        edo_batchWindowDesign.Ui_edo_batchWindow.setupUi(self,edo_batchWindow)
        #self.basicCtrl_bt.setText(_fromUtf8("aaaaa"))
        #self.IkFkChainCtrlTool_Bt.clicked.connect(self.IkFkChainCtrlTool_Bt_cmd_)
        #self.listText=dragLabelArea(self.fileList)
        self.saveToThisPath.clicked.connect(self.saveToThisPathClickCmd)
        self.batchBt.clicked.connect(self.batchBtCmd)
        
    def saveToThisPathClickCmd(self):
        print "saveToThisPathClick..."
        if self.saveToThisPath.isChecked():
            self.savePath.setEnabled(1)
            self.savePath.setStyleSheet(("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(180, 180, 180, 255), stop:1 rgba(250, 250, 250, 200))"))
        else:
            self.savePath.setEnabled(0)
            self.savePath.setStyleSheet(("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.142045 rgba(80, 80, 80, 255), stop:1 rgba(120, 120, 120, 200))"))

    def batchBtCmd(self):
        print "batchBtCmd..."
        #print 'python PyQt4 path: '+qtpath
        filelist=self.getAllFileIntoList()
        #print filelist
        script1=str(self.script1.text())
        #script2=str(self.script2.text())
        #script3=str(self.script3.text())
        #print script1+"\n"
        #print script2+"\n"
        #print script3+"\n"
        savepath=str(self.savePath.text())
        print 'save path:   ' + savepath+"\n"
        for f in filelist:
            print f+'\n'
            if os.path.isdir(f):
                print f +' ... is a path, not a file.pass...'
                continue
            if f[-3:]=='.ui':
                print 'turn <ui> to <py>'
                uic=qtpath+'pyuic4.bat'
                cmd=uic+' -o '+f.replace('.ui','.py')+' '+f
                print cmd
                os.system(cmd)
                if not savepath=='':
                    print 'copy file to specific path...'
                    shutil.move(f.replace('.ui','.py'),savepath)
            if f[-3:]=='.py':
                print 'turn <py> to <pyc>'
                compiler.compileFile(f)
                if not savepath=='':
                    print 'copy file to specific path...'
                    shutil.move(f.replace('.py','.pyc'),savepath)
            if f[-4:]=='.qrc':
                print 'turn <qrc> to <py>'
                qrc=qtpath+'pyrcc4.exe'
                cmd=qrc+' -o '+f.replace('.qrc','')+'_rc.py'+' '+f
                print cmd
                os.system(cmd)
                if not savepath=='':
                    print 'copy file to specific path...'
                    shutil.move(f.replace('.qrc','')+'_rc.py',savepath)
            if f[-3:]=='.ma':
                print 'use script modify ma'
                exe=self.getExePath()
                cmd=self.buildCmd()
                bat=exe+' -batch -file '+f+' -command '+cmd
                print 'bat:'+bat+'\n'
                #os.system(bat)
            if f[-3:]=='.mb':
                print 'use script modify mb'
                exe=self.getExePath()
                cmd=self.buildCmd()
                bat=exe+' -batch -file '+f+' -command '+cmd
                print 'bat:'+bat+'\n'
                #os.system(bat)
                
    def getAllFileIntoList(self):
        filetext=str(self.listText.text())
        #print filetext
        filelist=filetext.split('\n')
        return filelist

    def buildCmd(self):
        print 'buildCmd:'
        cmd=''
        scripttext=str(self.script1.text())
        scripttext=scripttext.replace('\n','')
        print scripttext
        #print scripttext[0]
        #print scripttext[-4:]
        if scripttext[-3:]=='.py':
            print 'python script'
            cmd='python("execfile(\\"'+scripttext+'\\")")'
        if scripttext[-4:]=='.mel':
            print 'mel script'
            cmd=scripttext
        print cmd
        return cmd

    def getExePath(self):
        print 'getExePath:'
        exepath=''
        exetext=str(self.exe.text())
        exetext=exetext.replace('\n','')
        print exetext
        return exetext
            

app=QtGui.QApplication(sys.argv)
ui=edo_batchWindow()
qtwindow=QtGui.QMainWindow()
ui.setupUi(qtwindow)
qtwindow.show()
app.exec_()
