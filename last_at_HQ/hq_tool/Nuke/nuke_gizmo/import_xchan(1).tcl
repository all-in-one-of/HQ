## -*- mode: tcl -*-
# Copyright (c) 2007 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Read a .chan file into the current node which should be a Camera or
# Axis.

# read data from a camera chan file:
# format is: FRAME TX TY TZ RX RY RZ VFOV
# If file contains fewer columns than only those columns are read


# Changed by Felix 2011

proc import_chan_file {filename} {

  set not_camera ![exists vaperture]

  if !$not_camera {
      set va [value vaperture]
  }

  catch {animation translate.x clear}
  catch {animation translate.y clear}
  catch {animation translate.z clear}
  catch {animation rotate.x clear}
  catch {animation rotate.y clear}
  catch {animation rotate.z clear}
  catch {animation focal clear}
  catch {animation haperture clear}


  set f [open $filename r]
  set n 0

  set trx ""
  set try ""
  set trz ""
  set rotx ""
  set roty ""
  set rotz ""
  set hfov ""

  while {[gets $f line]>=0} {
      if {[llength $line] < 4} continue
      incr n
      set fr [lindex $line 0]

      append trx $fr " " [lindex $line 1] " "
      append try $fr " " [lindex $line 2] " "
      append trz $fr " " [lindex $line 3] " "

      if {[llength $line] < 7 } {
          continue
      }

      append rotx $fr " " [lindex $line 4] " "
      append roty $fr " " [lindex $line 5] " "
      append rotz $fr " " [lindex $line 6] " "
      append hfov $fr " " [lindex $line 7] " "

      if {[llength $line] < 9 } {
          continue
      }

      if $not_camera continue
      setkey focal $fr "([lindex $line 8])"

  }
  close $f

  setkeys translate.x $trx
  setkeys translate.y $try
  setkeys translate.z $trz

  setkeys rotate.x $rotx
  setkeys rotate.y $roty
  setkeys rotate.z $rotz

  setkeys haperture $hfov

  # Turn off selectable flag so user doesn't destroy animation accidently:
  catch {knob selected false; knob selectable false}
  #$va / 2.0) / (tan(radians( [lindex $line 7] / 2.0 )
  # Save the filename into the node's label so user knows
  # where data came from.  This concats onto the existing label currently.
  catch {knob label [file tail $filename]}

  return "Loaded $n frames."
}

