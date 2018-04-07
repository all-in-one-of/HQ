# Written by Ali 2008
# www.2d3d.by
# Version 2.1
#
# get_node_source.tcl is required
# save_copy_as.tcl is required


proc render {_list} {
    
    global WIN32
    global env
    global program_name
    global threads
    set isLocal false
    
    #add render settings to Root
    add_render_settings
    if {$_list == 0} {return} 
    
    #save settings in variables
    set render_LaunchMode [value root.render_LaunchMode]
    set render_FrameRange [value root.render_FrameRange]
    set render_License [value root.render_License]
    set render_Cleanup [value root.render_Cleanup]
    set render_Priority [value root.render_Priority]
    set render_ShellThreads [expr abs([value root.render_ShellThreads])]
    if {$render_ShellThreads==0} {set render_ShellThreads $threads}
    set render_ParallelProcesses [expr abs([value root.render_ParallelProcesses])]
    set render_Mode [value root.render_Mode]
    set render_Threads [expr abs([value root.render_Threads])]
    if {$render_Threads==0} {set render_Threads $threads}
    set render_TaskFrames [expr abs([value root.render_TaskFrames])]
    set render_Pause [value root.render_Pause]
    set LicenseArg ""
    if {$render_License} {set LicenseArg "-i "}
    
    
    #check if path is local
    foreach n [nodes] {
        if {([class $n]=="Write" || [class $n]=="Read" || [class $n]=="ReadGeo2" || [class $n]=="ReadGeo" || [class $n]=="WriteGeo") && ![knob $n.disable]} {
            if {!$isLocal} {set isLocal [isPathLocal [file normalize [filename $n]]]}
        }
    }
    #check if script path is local
    if {!$isLocal} {set isLocal [isPathLocal [file normalize [knob root.name]]]}
    
    #element manager data gathering
    foreach n $_list {
        if {[class $n]=="Write" && ![value $n.disable]} {
            lappend write_list [knob $n.name]
        }
    }
    
    #check if exist write nodes
    if {![info exists write_list]} {
        message "No Write nodes"
        return 
    }

    #alphabet sorting
    set write_list [lsort -dictionary $write_list]
    
    set writeno 0
    foreach n $write_list {
        # add info to array and increase counter
        set write($writeno) [knob $n.name]
        incr writeno
    }

    #render order sorting
    if {[array size write]>1} {
        for {set y 0} {$y < [array size write]} {incr y} {
            set ok 1
            for {set x 0} {$x < [expr [array size write]-1]} {incr x} {
                set node [lindex [array get write $x] 1]
                set next_node [lindex [array get write [expr $x+1]] 1]
                if {[value $node.render_order]>[value $next_node.render_order]} {
                    set write($x) $next_node
                    set write([expr $x+1]) $node
                    set ok 0 
                }
            }
            if {$ok} break;
        }
    }
    
    #build GUI
    set args ""
    set totalframes 0    
    for {set x 0} {$x < [array size write]} {incr x} {        
        set node [lindex [array get write $x] 1]
        #add writeframes array alements
        set use_limit 0
        if [exists $node.use_limit] {set use_limit [value $node.use_limit]}
        if {$use_limit} {
            #set ranges to Writer's frame range limit (nuke6.1)
            set writeframes($x) [value $node.first],[value $node.last]
        } elseif {$render_FrameRange == "Global"} {
            #set ranges to global
            set writeframes($x) [value root.first_frame],[value root.last_frame]
        } else {
            #set ranges to input
            set writeframes($x) [expr int([value $node.first_frame])],[expr int([value $node.last_frame])]
        }
        set writefile($x) [filename $node]
        lappend args "\"<caption align=right>$node: [file tail [filename $node]] \" writeframes($x)"
    }
    lappend args {buttons "Cancel" "Ok"}
    
    set button    0
    #build title
    set title "Render with $render_LaunchMode"
    
    set tmpRender_Mode $render_Mode
    if {$render_Mode == "Auto"} { 
        if {$isLocal} {set tmpRender_Mode "Local"} else {set tmpRender_Mode "Remote"}
    } 
    if {$render_LaunchMode=="Alfred"} {append title " ($tmpRender_Mode)"}
    
    #show panel
    if [catch {set button [panel $title $args]}] {return}

    # Launch Modes switch
    switch -glob -- $render_LaunchMode {
    
    ##### NukeGUI Launch Script Mode ###############################################
    "NukeGUI" {
        if {$button!=1} {return}
        
        for {set x 0} {$x < [array size write]} {incr x} {
             
             set node [lindex [array get write $x] 1]
            
            #make dir if not exist
            make_dir [filename $node]
            
            #execution
            execute $node [lindex [array get writeframes $x] 1]
        }
    }

    
    ##### Shell Launch Script Mode ###############################################
    "Shell" {
        if {![file exist [file normalize [knob root.name]]]} {
            set nk_script "[getenv TEMP]/untitled.nk"
        } else {
            set nk_script [file normalize [file rootname [knob root.name]]]
        }
        
        set nuke_exe [file tail $program_name]
        
        #save current frame
        set cur_frame [frame]
        # set current frame to -1 so readers and writers won't conflict
        frame -1
        
        #create script copy
        set nk_script [file normalize [file join [file dirname $nk_script] [file tail $nk_script]_[date %y][date %m][date %d]_[date %H][date %M][date %S]]]
        append cmd_script $nk_script ".cmd"
        append nk_script ".nk\~"
        
        save_copy_as $nk_script
        puts "\nSave nuke script copy as ../[file tail $nk_script]"
        
        # set current frame to the saved one
        frame $cur_frame
        
        
        #build script lines
        set line "\@echo off\n"
        append line "echo Nuke render checkpoint [date %Y]/[date %m]/[date %d] [date %k]:[date %M]:[date %S]\n"
        append line "\n"
        
        for {set x 0} {$x < [array size write]} {incr x} {
            
            set node [lindex [array get write $x] 1]         
            set file_tail [file tail [filename $node]]
            
            #make dir if not exist
            make_dir [filename $node]

            # get frame ranges
            set last 0
            set step 1
            scan [lindex [array get writeframes $x] 1] %d%c%d%c%d first {} last {} step
            if {$first > $last} {set last $first}
            
            # if not sequence(avi, mov...)
            if [isNotSequence [filename $node]] {
                append line "start \"[file tail [knob root.name]] $node $first-$last\" /[value root.render_Priority] /wait \"$program_name\" -t $LicenseArg-m $threads -X $node \"$nk_script\" $first,$last,$step\n"
                continue
            }

            # do not use parallel tasks...
            if {$render_ParallelProcesses == 0} {
                append line "start \"[file tail [knob root.name]] $node $first-$last\" /[value root.render_Priority] /wait \"$program_name\" -t $LicenseArg-m $render_ShellThreads -X $node \"$nk_script\" $first,$last,$step\n"
                continue
            }
            
            # use one parallel task per writer...
            if {$render_ParallelProcesses == 1} {
                append line "start \"[file tail [knob root.name]] $node $first-$last\" /[value root.render_Priority] \"$program_name\" -t $LicenseArg-m $render_ShellThreads -X $node \"$nk_script\" $first,$last,$step\n"
                continue
            }
            
            # use parallel tasks...
            set tasks [expression ceil(($last-$first+1)/$render_ParallelProcesses)]
            for {set task_first $first} {$task_first <= $last} {incr task_first $tasks} {
                set task_last [expr $task_first + $tasks - 1]
                if {$task_last>$last} {set task_last $last}
                
                append line "start \"[file tail [knob root.name]] $node $task_first-$task_last\" /[value root.render_Priority] \"$program_name\" -t $LicenseArg-m $render_ShellThreads -X $node \"$nk_script\" $task_first,$task_last,$step\n"
            }
            
        }
        append line "\n"
        
        
        #delete temp files...
        if {$render_Cleanup} {
            if {$render_ParallelProcesses == 0} {
                append line "\ndel /f \"[regsub -all "\/" $nk_script "\\\\"]\"\n"
            }
            append line "del /f \"[regsub -all "\/" $cmd_script "\\\\"]\"\n"
        }
        
        append line "exit"
        
        #append script lines to saved script
        set fileid [open $cmd_script w]    
        puts $fileid $line
        close $fileid
        
        #set cmd_script [regsub -all "\/" $cmd_script "\\\\\\"]
        
        #execute script...
        puts $cmd_script
        if {$button==1} {
            #eval "exec cmd /c start \"Nuke \" \"$cmd_script\" &"
            eval "exec cmd /c \"$cmd_script\" &"
            puts "Render with Shell...\n"
        }
    }

    
    ##### Alfred Launch Script Mode ###############################################
    "Alfred" {
        if {![file exist [file normalize [knob root.name]]]} {
            set nk_script "[getenv TEMP]/untitled.nk"
        } else {
            set nk_script [file normalize [file rootname [knob root.name]]]
        }
        
        set nuke_exe [file tail $program_name]
        set alfred_path $env(RATTREE)
        append alfred_path "/bin/alfred"
        set alfred_path [regsub -all "\\\\" $alfred_path "\/"]
        set alfred_path [file normalize $alfred_path]
        set alf_command RemoteCmd
        if {$tmpRender_Mode == "Local"} {set alf_command Cmd}

        #save current frame
        set cur_frame [frame]
        # set current frame to -1 so readers and writers won't conflict
        frame -1
        
        #create script copy
        set nk_script "[file dirname $nk_script]/[file tail $nk_script]_[date %y][date %m][date %d]_[date %H][date %M][date %S]"
        append alf_script $nk_script ".alf"
        append nk_script ".nk\~"
        
        save_copy_as $nk_script
        puts "\nSave nuke script copy as ../[file tail $nk_script]"
        
        #set current frame to the saved one
        frame $cur_frame
        
        set shortname [file tail [knob root.name]]
        
        #build script lines
        set line "\#\#"
        append line "AlfredToDo 3.0 checkpoint [date %Y]/[date %m]/[date %d] [date %k]:[date %M]:[date %S]\n"
        append line "\# spooled as: $alf_script\n"
        append line "\# last estimated time remaining: +0:00:10\n\n"
        append line "Job -title {$shortname \(nuke render job\)}\\\n"
        append line "  -comment {Created by render script} \\\n"
        append line "  -elapsed 2 -etalevel 0 \\\n"
        append line "  -atleast 1 -atmost 3 -pbias 0 \\\n"
        append line "  -service {} -tags {} \\\n"
        append line "  -init \{\n"
        append line "    Assign txCmd {txmake}\n"
        append line "    Assign txSvc {}\n"
        append line "    Assign txTag {}\n"
        append line "  \} \\\n"
        append line "  -subtasks \{\n"
        
        for {set x 0} {$x < [array size write]} {incr x} {
        
            set node [lindex [array get write $x] 1]
            
            #make dir if not exist
            make_dir [filename $node]
            
            #executions...
            set last 0
            set step 1
            scan [lindex [array get writeframes $x] 1 ] %d%c%d%c%d first {} last {} step
            if {$first > $last} {set last $first}

            if [isNotSequence [filename $node]] {
            
                append line "         Task \{$node $first-$last\} -id \{${node}_$first\} -service \{nuke\} -tags \{nuke\}\\\n" 
                append line "             -cmds \{ $alf_command \{$nuke_exe -t $LicenseArg-m $threads -X [lindex [array get write $x] 1] \"$nk_script\" $first,$last,$step\} -refersto \{${node}_$first\} \}\n"
            
            } elseif {$render_TaskFrames == 0} {
            
                append line "         Task \{$node $first-$last\} -id \{${node}_$first\} -service \{nuke\} -tags \{nuke\}\\\n" 
                append line "             -cmds \{ $alf_command \{$nuke_exe -t $LicenseArg-m $render_Threads -X [lindex [array get write $x] 1] \"$nk_script\" $first,$last,$step\} -refersto \{${node}_$first\} \}\n"
                
            } else {
            
                set tmpTaskFrames [expr $render_TaskFrames - 1]
                append line "    Iterate frame -from $first -to $last -by $render_TaskFrames -template \{\n"
                append line "      Task \{$node \$frame-\[expr (\$frame+$tmpTaskFrames)>$last?$last:(\$frame+$tmpTaskFrames)\]\}\\\n"
                append line "        -id \{${node}_\$frame\}\\\n"
                append line "        -service \{nuke\}\\\n"
                append line "        -tags \{nuke\}\\\n" 
                append line "        -cmds \{ $alf_command \{$nuke_exe -t $LicenseArg-m $render_Threads -X [lindex [array get write $x] 1] \"$nk_script\" \$frame,\[expr (\$frame+$tmpTaskFrames)>$last?$last:(\$frame+$tmpTaskFrames)\]\} -refersto \{${node}_\$frame\}\}\n" 
                append line "    \}\n"
                
            }
        }
        append line "  \}"
        
        if {$render_Cleanup} {
            append line " \\\n  -cleanup \{\n"
            append line "    Cmd {Alfred} -msg {File delete \"$nk_script\" \"$alf_script\"}\n"
            append line "  \}"
        }
        append line "\n"
        append line "\#\# --- End of Job '$shortname \(nuke render job\)'\n"
        
        #append script lines to saved script
        if {[catch {set fileid [open $alf_script w]} result_alf_script_save ]} {error $result_alf_script_save; return}
        puts $fileid $line
        close $fileid
        
        #execute script...
        if {$button==1} {
            set alf_execute "exec cmd.exe /c $alfred_path.exe "      
            if {$render_Pause} {append alf_execute "-paused "}
            append alf_execute $alf_script
            append alf_execute " &"    
            if {[eval $alf_execute]} {puts "Render with Alfred..."}
        }
    }
    }
    
    return
}


# -------------------------------------------------------------------------------------------
# add render settings to root
proc add_render_settings {} {
    in root {    
        # Initialization
        set render_LaunchMode "NukeGUI"
        if [exists render_LaunchMode] {set render_LaunchMode [value render_LaunchMode]}
        set render_FrameRange "Global"
        if [exists render_FrameRange] {set render_FrameRange [value render_FrameRange]}
        set render_License 0
        if [exists render_License] {set render_License [value render_License]}
        set render_Cleanup 1
        if [exists render_Cleanup] {set render_Cleanup [value render_Cleanup]}
        set render_Priority "Normal"
        if [exists render_Priority] {set render_Priority [value render_Priority]}
        set render_ShellThreads 0
        if [exists render_ShellThreads] {set render_ShellThreads [value render_ShellThreads]}
        set render_ParallelProcesses 0
        if [exists render_ParallelProcesses] {set render_ParallelProcesses [value render_ParallelProcesses]}
        set render_Mode "Local"
        if [exists render_Mode] {set render_Mode [value render_Mode]}
        set render_Threads 1
        if [exists render_Threads] {set render_Threads [value render_Threads]}
        set render_TaskFrames 1
        if [exists render_TaskFrames] {set render_TaskFrames [value render_TaskFrames]}
        set render_Pause 0
        if [exists render_Pause] {set render_Pause [value render_Pause]}
        
        # Remove knobs
        #remove_render_settings
        
        # Add knobs and set values
        addUserKnob {20 Render l "Render"}
        addUserKnob {4 render_LaunchMode l "launch script mode" M {NukeGUI Shell Alfred}}
        knob render_LaunchMode $render_LaunchMode
        addUserKnob {32 render_Button l " RENDER " -STARTLINE T "if \[catch \{set seln \[selected_nodes]\}] \{\nrender \[nodes]\n\} else \{\nrender \$seln \n\} "}
        addUserKnob {4 render_FrameRange l "frame range" M {Global Input}}
        knob render_FrameRange $render_FrameRange
        addUserKnob {6 render_License l "use interactive license" +STARTLINE}
        knob render_License $render_License
        addUserKnob {6 render_Cleanup l "cleanup temp files" +STARTLINE}
        knob render_Cleanup $render_Cleanup        
        # Shell group
        addUserKnob {20 render_ShellGroup l "Shell settings..." n 1}
        knob render_ShellGroup 0
        addUserKnob {4 render_Priority l "process priority" -STARTLINE M {Normal Low}}
        knob render_Priority $render_Priority
        addUserKnob {3 render_ShellThreads l "thread count" t "Number of threads for each process.\n0 - use number of CPUs. "}
        knob render_ShellThreads $render_ShellThreads
        addUserKnob {3 render_ParallelProcesses l "parallel processes" t "Number of parallel processes.\n0 - don't use parallel processes\n1 - use one parallel process for each write node\nand etc."}
        knob render_ParallelProcesses $render_ParallelProcesses
        addUserKnob {20 render_ShellEndGroup l endGroup n -1}
        # Alfred group
        addUserKnob {20 render_AlfredGroup l "Alfred settings..." n 1}
        knob render_AlfredGroup 0
        addUserKnob {4 render_Mode l "mode" -STARTLINE M {Local Remote Auto}}
        knob render_Mode $render_Mode
        addUserKnob {3 render_Threads l "thread count" t "Number of threads for each task.\n0 - use number of CPUs. "}
        knob render_Threads $render_Threads
        addUserKnob {3 render_TaskFrames l "frames per task" t "Number of frames to render whith one task.\n0 - use one task for each write node."}
        knob render_TaskFrames $render_TaskFrames
        addUserKnob {6 render_Pause l "start render manager paused" +STARTLINE}
        knob render_Pause $render_Pause
        addUserKnob {20 render_AlfredEndGroup l endGroup n -1}
    }
}


# ----------------------------------------------------------------------------------------------
# remove render settings
proc remove_render_settings {} {
    foreach knob_name [knobs root] {
        if [string first "render_" $knob_name] {continue}
        python "nuke.root().removeKnob(nuke.root().knob('$knob_name'))"
    }
    
    if [exists root.Render] {python "nuke.root().removeKnob(nuke.root().knob('Render'))"}
    if [exists root.render_AlfredEndGroup] {python "nuke.root().removeKnob(nuke.root().knob('render_AlfredEndGroup'))"}
    if [exists root.render_ShellEndGroup] {python "nuke.root().removeKnob(nuke.root().knob('render_ShellEndGroup'))"}
    if [exists root.endGroup_alfred] {python "nuke.root().removeKnob(nuke.root().knob('endGroup_alfred'))"}
}


# ----------------------------------------------------------------------------------------------
# checks if path is local
proc isPathLocal {path} {
    return [string compare -nocase -length 2 $path "//"]
}


# ----------------------------------------------------------------------------------------------
# check if filename is not sequence but avi, mov, mpg, flv, mp4 ...
proc isNotSequence {filename} {
    set ext [string tolower [file extension $filename]]
    if {$ext==".avi" || $ext==".mov" || $ext==".mpg" || $ext==".flv" || $ext==".mp4" || $ext==".wmv" || $ext==".r3d"} {return 1}    
    return 0
}


# ----------------------------------------------------------------------------------------------
# get the frame number out of cancelled error message
proc extract_cancel {msg} {
    if ![string match "Cancel*" $msg] {return 0}
    if {[llength $msg]<2} {return 0}
    return [lindex $msg 1]
}


# ----------------------------------------------------------------------------------------------
# make dir
proc make_dir {filename} {
    #make dir if not exist (check if use stereo symbol %V or %v in folder name)

    set dir [file dirname $filename]
    foreach {view color} [value root.views] {
        set dir0 [regsub -all "\%V" $dir $view]
        set dir0 [regsub -all "\%v" $dir0 [lindex $view 0]]
        catch {file mkdir $dir0}
    }
}
