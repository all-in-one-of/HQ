# -*- coding: UTF-8 -*- 
# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Modyfied by Adrian Baltowski

################################ menu.py ###########################
"""

import audioToFramecycler

renderbar=nuke.menu("Nuke").findItem("Render")
renderbar.addSeparator()
aaa=renderbar.addCommand('Flipbook With Audio', 'audioToFramecycler.flipbook_with_audio(nuke.selectedNode())', "shift+alt+f")
if nuke.env['ple']:
   aaa.setEnabled(False)

"""
################################ END of menu.py ######################################


import re
import os.path
import nuke
import platform
import sys
import thread
import subprocess


previous_inrange = ""
previous_userrange = ""
previous_audio = ""

def flipbook_with_audio(node, framesAndViews = None):
  """Runs an arbitrary command on the images output by a node. This checks
  to see if the node is a Read or Write and calls the function directly
  otherwise it creates a temporary Write, executes it, and then calls
  the command on that temporary Write, then deletes it.
  
  By writing your own function you can use this to launch your own
  flipbook or video-output programs.
  
  Specify framesAndViews as a tuple if desired, like so: ("1,5", ["main"])
  This can be useful when running without a GUI."""

  # Stop here if we're trying to Framecycle in PLE mode, as in some code paths
  # the execute is called before the Framecycler script could do this check
  if nuke.env['ple']:
    raise RuntimeError("Framecycler is not available in PLE mode.")
  
  global previous_inrange
  global previous_userrange
  global previous_audio

  if node is None or (node.Class() == "Viewer" and node.inputs() == 0): return

  a = int( nuke.numvalue(node.name()+".first_frame") )
  b = int( nuke.numvalue(node.name()+".last_frame") )
  if a >= b:
    a = int( nuke.numvalue("root.first_frame") )
    b = int( nuke.numvalue("root.last_frame") ) 

  try:
    inrange= str( nuke.FrameRange(a, b, 1) )
  except ValueError,e:
    # In this case we have to extract from the error message the
    # correct frame range format string representation.
    # I'm expecting to have a error like: "Frame Range invalid (-1722942,-1722942)"
    
    msg = e. __str__()
    inrange = msg[ msg.index("(")+1:  msg.index(")") ]
  
  if inrange == previous_inrange: inrange = previous_userrange

  #following is from me

	
  if framesAndViews is None:
    p = nuke.Panel("Frames to Flipbook: ", 400)
    view = nuke.views()
    selectedViews = []
    audio = ""
    if previous_audio != "" and os.path.isfile(previous_audio):
      audio = previous_audio
    stereo = framecycler_stereo_available_()

    p.addSingleLineInput("Frames", inrange)
    p.addFilenameSearch("Audio file...", audio)
    if len(view) > 1:
      if stereo:
        booleanCheckBox = True
        for n in view:
          p.addBooleanCheckBox((n+" view"), booleanCheckBox)
      else:
        strr=""
        for n in view:
          strr = strr+(str(n)+" ")
        p.addEnumerationPulldown("views:", strr)

    p.addButton("Cancel")
    p.addButton("OK")

    panelResult = p.show()

    if panelResult == 0:
      return

    else:
      range_input = p.value("Frames")
      audio_file = p.value("Audio file...")

      if len(view) > 1:
        if stereo:
          for m in view:
            boolVal = p.value((m+" view"))
            if boolVal is True:
              selectedViews.append(m)
            else:
              continue
          views_input = selectedViews
        else:
          selectedViews.append(p.value("views:"))
          views_input = selectedViews
      else:
        views_input = view
  else:
    r = framesAndViews
    range_input = r[0]
    views_input = r[1]

  previous_inrange = inrange  
  previous_userrange = range_input
  previous_audio = audio_file
  
  f = nuke.FrameRange( range_input )
  
  start =f.first() 
  end = f.last()
  incr = f.increment()
  
  if (start) < 0 or (end<0):
    raise RuntimeError("Flipbook cannot be executed, negative frame range not supported(%s)." % ( str(f),) )
  
  proxy = nuke.toNode("root").knob("proxy").value()

  if (node.Class() == "Read" or node.Class() == "Write") and not proxy:
    try:
      framecycler_this_with_audio(node, start, end, incr, views_input, audio_file)
    except Exception, msg:
      nuke.message("Error running flipbook:\n%s" % (msg,))
    return

  if node.Class() == "Viewer":
    input_num = int(nuke.knob(node.name()+".input_number"))
    input = node.input(input_num)
    if input is None: return

    if (input.Class() == "Read" or input.Class() == "Write") and not proxy:
      try:
        framecycler_this_with_audio(input, start, end, incr, views_input, audio_file)
      except Exception, msg:
        nuke.message("Error running flipbook:\n%s" % (msg,))
      return

  # okay now we must execute it...
  flipbooktmp=""
  if flipbooktmp == "":
    try:
      flipbooktmp = os.environ["FC_DISK_CACHE"]
    except:
      try:
        flipbooktmp = os.environ["NUKE_DISK_CACHE"]
      except:
        flipbooktmp = nuke.value("preferences.DiskCachePath")
  
  if len(views_input) > 1:
    flipbookFileNameTemp = "nuke_tmp_flip.%04d.%V.rgb"
  else:
    flipbookFileNameTemp = "nuke_tmp_flip.%04d.rgb"
  flipbooktmp = os.path.join(flipbooktmp, flipbookFileNameTemp)
  
  if nuke.env['WIN32']:
    flipbooktmp = re.sub("\\\\", "/", str(flipbooktmp))

  fieldname="file"
  if proxy:
    fieldname="proxy"

  write = nuke.createNode("Write", fieldname+" {"+flipbooktmp+"} "+"tile_color 0xff000000", inpanel = False)
  #If called on a Viewer connect Write node to the one immediately above if exists.
  if node.Class() == "Viewer":
    write.setInput(0, node.input(int(nuke.knob(node.name()+".input_number"))))

  try:
    # Throws exception on render failure
    nuke.executeMultiple((write,), ([start,end,incr], ), views_input)
    framecycler_this_with_audio(write, start, end, incr, views_input, audio_file)
  except Exception, msg:
    nuke.message("Flipbook render failed:\n%s" % (msg,))
  nuke.delete(write)




def framecycler_stereo_available_():
  """Returns True iff the current platform supports the stereo version of FrameCycler (i. e. Windows, Linux or OS X 10.5 or
  higher), or False otherwise."""
  if not nuke.env['MACOS']:
    return True                   # Windows or Linux
  ver = platform.mac_ver()[0]
  # OS X
  try:
    if float(ver[:4]) >= 10.5:
      return True               # OS X Leopard or higher
  except:
    pass
  return False                    # OS X Tiger or lower


def run_app_(app, in_args):
  args = [app]
  for a in in_args:
    args.append(a)
  try:
    p = subprocess.Popen(args=args, executable=app, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = p.communicate()
    return output
  except:
    return ""

def framecycler_linux_version_():
  if nuke.NUKE_VERSION_MAJOR >= 6 and nuke.NUKE_VERSION_MINOR >= 1:
    default_path = "CentOS5"
  else:
    default_path = "CentOS4.4"
  output = run_app_("/usr/bin/lsb_release",  ["-a"])
  if len(output) == 0:
    output = run_app_("/usr/local/bin/lsb_release", ["-a"])
    if len(output) == 0:
      output = run_app_("/bin/lsb_release", ["-a"])
      if len(output) == 0:
        return default_path
  try:
    if output.find('CentOS') >= 0:
      match = re.search('Release:\s*[\d.]+', output)
      if match != None:
        substring = match.group(0)
        versionMatch = re.search('[\d.]+', substring)
        versionString = versionMatch.group(0)
        if (float(versionString)) < 5.0:
          return "CentOS4.4"
  except:
    pass
  return default_path

my_fc_path=""
if my_fc_path == "":
  try:
    my_fc_path = os.environ["FC_PATH"]
  except:
    try:
      my_fc_path = os.path.join(os.environ["FC_HOME"], "bin", "framecycler")
    except:
      my_fc_path = os.path.join(os.path.dirname(nuke.EXE_PATH), "FrameCycler")
      fc_suffix = ""
      if nuke.env['WIN32']:
        my_fc_path = os.path.join(my_fc_path+"Windows", "bin", "framecycler")
      elif not nuke.env['WIN32'] and not nuke.env['MACOS']:
        my_fc_path = os.path.join(my_fc_path+framecycler_linux_version_(), "bin", "framecycler")
      else:
        my_fc_path = os.path.join(my_fc_path + "OSX", "bin", "FrameCycler")
  if nuke.env['WIN32']:
      my_fc_path = my_fc_path + ".exe"


def framecycler_sequence_(frange, filename, cmd_args_size):
  sequence = []
  for i in xrange(min(frange.frames(), cmd_args_size)):
    sequence.append( "Q[" )
    sequence.append( filename )
    sequence.append( "%d-%d" % (frange.getFrame(i), frange.getFrame(i)) )
    sequence.append( "]Q" )
  return sequence

def framecycler_this_with_audio(node, start, end, incr, view, audio_file):
  """Run framecycler on a Read or Write node. See the flipbook command
  for how we run framecycler on *any* node."""
  
  global my_fc_path

  audio_filename = ""


  if not os.access(my_fc_path, os.X_OK):
    raise RuntimeError("Framecycler cannot be executed (%s)." % (my_fc_path,) )

  filename = nuke.filename(node)
  if filename is None or filename == "":
    raise RuntimeError("Framecycler cannot be executed on '%s', expected to find a filename and there was none." % (node.fullName(),) )


  if node.Class() == "Write" and node['file_type'].value() == "mov":
    if node['audiofile'].value() != "" and os.path.isfile(node['audiofile'].value()):
      audio_filename = node['audiofile'].value()
  elif audio_file != "" and os.path.isfile(audio_file):
    audio_filename = audio_file


  sequence_interval = str(start)+"-"+str(end)
  (filename, subs) = re.subn("(%[0-9]+)d", "#", filename)

  # if the step beetwen frames is bigger then one
  # we have to build the framecycler syntax in a special way
  # the idea is to add multiple queue sequence of 1 frame
  
  if subs == 0 or incr > 1:
    sequence_interval = ""

  (filename, subs) = re.subn("%V", view[0], filename)
  (filename, subs) = re.subn("%v", view[0][0], filename)
  
  os.path.normpath(filename)

  w = nuke.value(node.name()+".actual_format.width")
  h = nuke.value(node.name()+".actual_format.height")
  cropa = nuke.value(node.name()+".actual_format.x")
  cropb = nuke.value(node.name()+".actual_format.y")
  cropc = str(nuke.expression(node.name()+".actual_format.r"+"-"+cropa))
  cropd = str(nuke.expression(node.name()+".actual_format.t"+"-"+cropb))
  pa = nuke.value(node.name()+".actual_format.pixel_aspect")

  args = []
  my_fc_path = os.path.normpath(my_fc_path)
  if nuke.env['WIN32']:
    args.append( "\"" + my_fc_path + "\"" )
    filename = "\"" + filename + "\""
  else:
    args.append( my_fc_path )    



  if incr == 1:
    args.append(filename)	
    args.append(sequence_interval)

  if cropa is not None or cropb is not None or cropc != w or cropd != h:
    args.append("-c")
    args.append(cropa)
    args.append(cropb)
    args.append(cropc)
    args.append(cropd)

  resample = ""
  if float(pa)>1:
    args.append("-r")
    args.append("100%")
    args.append(str(int(100/float(pa)))+"%")
  elif float(pa)<1:
    args.append("-r")
    args.append(str(int(100/float(pa)))+"%")
    args.append("100%")

  root=nuke.toNode("root")
  fps=root.knob('fps').getValue()
  args.append("-f"+str(fps))

  if len(view) > 1:
    args.append("-stereo")
  	
  if incr > 1:
    # I didn't find any pyhon call that return the maximum argument size for command line.
    # I hope that 1000 is enough.
    maximun_cmd_args_size = 1000    
  
    frange =  nuke.FrameRange(start, end, incr)  
    sequence = framecycler_sequence_( frange, filename, maximun_cmd_args_size )                
    args += sequence

  if audio_filename != "":
    audio_filename = os.path.normpath(audio_filename)
    args.append("-s")
    if nuke.env['WIN32']:
      args.append( "\"" + audio_filename + "\"" )
    else:
      args.append(audio_filename)

  print args  
 
  nuke.IrToken()
  os.spawnv(os.P_NOWAITO, my_fc_path, args)

