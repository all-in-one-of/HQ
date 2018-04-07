#!/usr/bin/env python
#coding=cp936
#coding=utf-8

import pathforuser 
path = pathforuser.path_dir()+'/check/scripts/'
"""
if path not in sys.path :
	sys.path.append(path)
"""
import riggingCheck
reload(riggingCheck)


riggingCheck.run()