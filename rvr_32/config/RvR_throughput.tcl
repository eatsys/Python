cd D:/work/Reamon/Python/rvr/config
set config_work "D:/work/Reamon/Python/rvr/config"
#work改为config_work
source "$config_work/get_config.tcl"
set pcip [getConfig "config.ini" "chariot_config" "pc_ip"]
puts "$pcip"
set staip [getConfig "config.ini" "chariot_config" "sta_ip"]
puts "$staip"
set duration [getConfig "config.ini" "chariot_config" "duration"]
puts "$duration"
set pairNumber [getConfig "config.ini" "chariot_config" "pairnumber"]
puts "$pairNumber"
set atten [getConfig "config.ini" "chariot_config" "attenvalue"]
puts "$atten"
set angle [getConfig "config.ini" "compass_config" "angle"]
puts "$angle"

#lappend auto_path "C:/Program Files (x86)/Ixia/IxChariot"
#package require ChariotExt
#global auto_index
#eval $auto_index(ChariotExt)


#cd C:/Program Files (x86)/Ixia/IxChariot
set chariot_dir "C:/Program Files (x86)/Ixia/IxChariot"
#work_dir改为chariot_dir
set script "$chariot_dir/Scripts/High_Performance_Throughput.scr"

#cd D:/work/Reamon/Python/rvr/Result
set log_dir "D:/work/Reamon/Python/rvr/Result"

if {![file isdirectory $log_dir/IxChariotOD]} {
  file mkdir $log_dir/IxChariotOD
}
#set timeStamp [clock format [clock seconds] -format "%Y-%m-%d-%H-%M-%S"]
#set timeStamp 40
set result $log_dir/IxChariotOD/$atten
set tstResult ${result}.tst

load ChariotExt
package req ChariotExt

foreach {direct src dst} [subst {Tx $pcip $staip Rx $staip $pcip}] {
puts "Create the test..."
set test [chrTest new]

puts "Create the RunOptions..."
set runOpts [chrTest getRunOpts $test]

chrRunOpts set $runOpts TEST_END FIXED_DURATION
chrRunOpts set $runOpts TEST_DURATION $duration
puts "Test End Conditions: [chrRunOpts get $runOpts TEST_END]"

for {set i 0} {$i < $pairNumber} {incr i} {
	puts "Create pair$i..."
	set pair$i [chrPair new]

	puts "Set required pair attributes..."
	chrPair set [set pair$i] E1_ADDR $src E2_ADDR $dst

	puts "use a script..."
	chrPair useScript [set pair$i] $script

	puts "Add the pair to the test..."
	chrTest addPair $test [set pair$i]
}

puts "Run the test..."
chrTest start $test

puts "Wait for the test to stop..."
set done [chrTest isStopped $test]
while {!$done} {
	#wait 5 seconds if it stops
	set done [chrTest isStopped $test 5]	
}
puts "Save the test..."
set tstResult ${result}_$direct.tst
chrTest save $test $tstResult
set txtResult ${result}_$direct.txt
exec FMTTST $tstResult $txtResult
chrTest delete $test force
}

exit

