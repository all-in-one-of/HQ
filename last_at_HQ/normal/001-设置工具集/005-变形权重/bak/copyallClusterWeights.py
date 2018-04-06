import sys
path = u'//10.99.0.99/\u6570\u7801\u7535\u5f71/\u7535\u5f71\u4e2d\u5fc3/03\u52a8\u753b/\u5458\u5de5\u6587\u4ef6/L-\u6881 \u5eb8/\u6881\u5eb8mel\u63d0\u4ea4/\u7c07\u62f7\u6743\u91cd/2012'
if not path in sys.path:
	sys.path.append(path)
from copyallClusterWeights import *
win()