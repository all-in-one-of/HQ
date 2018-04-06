# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################


import os
for p in os.environ['path'].split(';'):
    if os.path.exists( os.path.join(p, 'houdinifx.exe') ):
        houdiniPath = os.path.dirname( p ).replace( '\\', '/' )
        #print houdiniPath
        break