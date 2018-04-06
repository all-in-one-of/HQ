__author__ = 'huangshuai'
import sys, pprint
from pysideuic import compileUi
pyfile = open("C:/Users/huangshuai/Documents/checkNodes/checkNodesWidget_ui.py", 'w')
compileUi("C:/Users/huangshuai/Documents/checkNodes/checkNodesWidget.ui", pyfile, False, 4,False)
pyfile.close()