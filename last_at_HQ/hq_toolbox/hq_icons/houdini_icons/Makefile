#!/bin/make -f

START   = archivemaker

DIRS	= \
	archivemaker \
	makearchive

makearchive: archivemaker

RESOURCEFILES = \
	IconMapping \
	LICENSE.txt

RESOURCEDIR = $(DEV_SUPPORT)/config

install::
	(cd $(RESOURCEDIR) ; rm -f $(RESOURCEFILES))
	cp $(RESOURCEFILES) $(RESOURCEDIR)
	(cd $(RESOURCEDIR) ; $(call CHMOD,a-w,$(RESOURCEFILES)))

include $(SRCROOT)/houdini/make/C++MakeDirs
