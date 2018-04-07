# -*- coding: utf-8 -*-
__author__ = 'SuQing','XuSiJian'
__date__    = '2017-03-20'
import json
import os
from PySide import  QtGui
from functools import partial
class taskBar(QtGui.QWidget):
    def __init__(self):
        super(taskBar, self).__init__()
        self.allMenu ={ }
        #self.sign = True
        #显示托盘图标
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.show()

        self.contextMenu  = QtGui.QMenu(self)
        self.trayIcon.setContextMenu(self.contextMenu )
        self.allMenu['root'] = self.contextMenu


        #双击托盘信号槽
        #self.trayIcon.activated(QtGui.QSystemTrayIcon.Context)
        self.updateMenu()
        self.trayIcon.activated.connect(self.updateMenu)
        #激活右键托盘菜单

    def actionExecute(self, execute, dialogInfo ):
        os.system( execute )
        if dialogInfo!=None:
            QtGui.QMessageBox.about(self, 'Famo configure', dialogInfo)


    def updateMenu(self):
        #Reset allMenu
        if self.allMenu:
            for key, qtObj in self.allMenu.iteritems():
                if key=='root':
                    continue
                if isinstance( qtObj, QtGui.QMenu):
                    qtObj.destroy( )
                else:
                    qtObj.deleteLater()
                del( qtObj )
        self.allMenu = {}
        self.allMenu['root'] = self.contextMenu
        self.contextMenu.clear()



        configureFile = open(u'O:/hq_tool/famo_configure/Resource/json/menuData.json', 'r')
        configureData = json.load(configureFile)
        configureFile.close()

        menuData = configureData['menuData']
        trayIconData = configureData['trayIconData']


        defaultIcon = trayIconData.get('defaultIcon', None)
        toolTip = trayIconData.get('toolTip', None)

        if defaultIcon:
            self.trayIcon.setIcon( QtGui.QIcon(defaultIcon) )

        if toolTip:
            self.trayIcon.setToolTip( toolTip )


        def createMenu( menu, parent='' ):
            rootParent = parent if parent else 'root'
            for smenu in menu:
                hasChildren = smenu.has_key( 'children' )
                hasicon = smenu.has_key( 'iconPath' )
                if hasicon:
                    iconpath, menuName,= smenu['iconPath'] , smenu['menuName']
                else:
                    iconpath, menuName, = defaultIcon, smenu['menuName']

                parent = rootParent + '/'+ menuName
                if rootParent=='root' or hasChildren:
                    self.allMenu[ parent ] = self.allMenu[rootParent].addMenu(QtGui.QIcon(iconpath),  menuName)
                else:
                    execute, dialogInfo = smenu['execute'], smenu['dialogInfo']
                    self.allMenu[parent] = self.allMenu[ rootParent ].addAction( QtGui.QIcon( iconpath),menuName)
                    self.allMenu[parent].triggered.connect( partial(self.actionExecute, execute, dialogInfo) )
                if hasChildren:
                    createMenu( smenu['children'], parent )

        createMenu( menuData )
        self.quitAction = self.contextMenu .addAction( u'退出')
        self.quitAction.triggered.connect(QtGui.qApp.quit)
        self.contextMenu .addAction(self.quitAction)
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window = taskBar()
    sys.exit(app.exec_())
