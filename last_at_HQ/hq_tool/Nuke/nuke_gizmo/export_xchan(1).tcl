# Copyright (c) 2007 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Write the animation from the current Camera or Axis node to a .chan file

proc export_chan_file {filename} {
  set start [animation_start]
  set increment [animation_increment]
  set end [animation_end]

  set not_camera ![exists this.vaperture]

  set f [open $filename w]
  for {set x $start} {$x<$end+1} {incr x} {
	set line $x\t
	append line [expression translate.x($x)]\t
	append line [expression translate.y($x)]\t
	append line [expression translate.z($x)]\t
	append line [expression rotate.x($x)]\t
	append line [expression rotate.y($x)]\t
	append line [expression rotate.z($x)]\t
	append line [expression haperture($x)]

	if $not_camera {
	  puts $f $line
	} else {
	  append line \t
	  set va [expression vaperture($x)]
	  set vao [expression focal($x)]
	  append line [expr $vao]
	  puts $f $line
	}
  }
  close $f
}
