# -*- coding: utf-8 -*-
docStr =     '''{'path':'Animation/removeFractionalKeys( )',
'path':'Animation',
'usage':"""
#删除选择物体的translate, rotate, scale, visibility的小数帧
$fun( )""",
}
    '''
#print eval( docStr.strip() )
try:
    docStr = eval( docStr.strip() )
except:
    print 'got error on docStr evaluate!'
    raise IOError()


cmdPath = docStr.get('path', None)
if True and not cmdPath:
    cmdPath = docStr.get( 'del_path', None )
if not cmdPath:
    print 2
print cmdPath

#funName = 'QM'+'.'+ eval( "%s.%s.__name__"%( 'ttt' ) )
#cmdPath = cmdPath + '/' + funName  + "()"

note = docStr.get( 'tip', None )
icon = docStr.get( 'icon', None )
print note, icon
#icon = icon.replace( '$ICONROOT', kwargs['iconRoot'] ) if icon else kwargs['defaultIcon']
#print icon
#helpDoc = docStr.get( 'help', None )
#cmdUI = funName+'_ui' if funName+'_ui' in uiList else None

#resultList[cmdPath] = [ note, icon ]