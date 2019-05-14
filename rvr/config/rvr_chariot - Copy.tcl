
#cd D:/work/Reamon/Python/rvr/config
set config_work "D:/rvr/config"
#work改为config_work
cd $config_work
source "$config_work/get_config.tcl"
set ap [getConfig "config.ini" "ap_config" "ap_type"]
string trim $ap
puts "AP:	$ap"
set radio [getConfig "config.ini" "ap_config" "radio"]
string trim $radio
puts "Radio:	$radio"
set channel [getConfig "config.ini" "ap_config" "channel"]
string trim $channel
puts "Channel:	$channel"
set pcip [getConfig "config.ini" "chariot_config" "pc_ip"]
string trim $pcip
puts "PC_IP:	$pcip"
set staip [getConfig "config.ini" "chariot_config" "sta_ip"]
string trim $staip
puts "STA_IP:	$staip"
set duration [getConfig "config.ini" "chariot_config" "duration"]
string trim $duration
puts "TEST_DURATION:	$duration"
set pairNumber [getConfig "config.ini" "chariot_config" "pair_number"]
string trim $pairNumber
puts "TEST_PAIRS:	$pairNumber"
set attenvalue [getConfig "config.ini" "chariot_config" "atten_value"]
string trim $attenvalue
puts "TEST_ATTENUATE:	$attenvalue"
set current_angle [getConfig "config.ini" "swivel_table_config" "current_angle"]
string trim $current_angle
puts "TEST_Angle:	$current_angle"

set log_dir "D:/rvr/Result"
if {![file isdirectory $log_dir/IxChariotOD/$ap]} {
  file mkdir $log_dir/IxChariotOD/$ap
}

set result $log_dir/IxChariotOD/$ap/${radio}_${channel}_${attenvalue}_$current_angle
set tstResult ${result}.tst

set IxChariot_installation_dir "C:/Program Files (x86)/Ixia/IxChariot"
#puts c:
cd $IxChariot_installation_dir

set script "C:/Program Files (x86)/Ixia/IxChariot/Scripts/High_Performance_Throughput.scr"
set timeout 5

load ChariotExt
package require ChariotExt

foreach {direct src dst} [subst {Tx $pcip $staip Rx $staip $pcip}] {
#puts $direct
puts "Create the test..."
set test [chrTest new]

puts "Create the RunOptions..."
set runOpts [chrTest getRunOpts $test]

chrRunOpts set $runOpts TEST_END FIXED_DURATION
chrRunOpts set $runOpts TEST_DURATION $duration
puts "Test End Conditions: [chrRunOpts get $runOpts TEST_END]"

for { set i 0}  {$i < $pairNumber} {incr i} {
	puts "Create pair$i..."
	set pair$i [chrPair new]

	puts "Set required pair attributes..."
	puts "$src"
	puts "$dst"
	chrPair set [set pair$i] E1_ADDR $src E2_ADDR $dst

	puts "Use a script..."
	chrPair useScript [set pair$i] $script

	puts "Add the pair to the test..."
	chrTest addPair $test [set pair$i]
	}
	
puts "Number of pairs = [chrTest getPairCount $test]"
puts "[chrPair get $pair1 E1_ADDR]"
puts "[chrPair get $pair1 E2_ADDR]"
puts "Protocol [chrPair get $pair1 PROTOCOL]"
puts "Script file [chrPair get $pair1 SCRIPT_FILENAME]"
#puts "Appl script name [chrPair get pair$i APPL_SCRIPT_NAME]"


puts "Run the test..."
chrTest start $test

puts "Wait for the test to stop..."
set done [chrTest isStopped $test]
while {!$done} {
	#wait 5 seconds if it stops
	set done [chrTest isStopped $test 5]	
}

#puts "Time [chrPair getTimingRecordCount $pair1]"
#set throughput1 [chrPairResults get $pair0 THROUGHPUT]
#set throughput2 [chrPairResults get $pair1 THROUGHPUT]
#set throughput3 [chrPairResults get $pair2 THROUGHPUT]
#set throughput4 [chrPairResults get $pair3 THROUGHPUT]
#set throughput5 [chrPairResults get $pair5 THROUGHPUT]
#set throughput6 [chrPairResults get $pair6 THROUGHPUT]
#set throughput7 [chrPairResults get $pair7 THROUGHPUT]
#set throughput8 [chrPairResults get $pair8 THROUGHPUT]
#
#set avg1 [format "%.3f" [lindex $throughput1 0]]
#set avg2 [format "%.3f" [lindex $throughput2 0]]
#set avg3 [format "%.3f" [lindex $throughput3 0]]
#set avg4 [format "%.3f" [lindex $throughput4 0]]
#set avg5 [format "%.3f" [lindex $throughput5 0]]
#set avg6 [format "%.3f" [lindex $throughput6 0]]
#set avg7 [format "%.3f" [lindex $throughput7 0]]
#set avg8 [format "%.3f" [lindex $throughput8 0]]
#
#set avg [expr $avg1 + $avg2 + $avg3 + $avg4 + $avg5 + $avg6 + $avg7 + $avg8]
#
#puts "Throughput:"
#puts "pair1 $avg1"
#puts "pair2 $avg2"
#puts "pair3 $avg3"
#puts "pair4 $avg4"
#puts "pair5 $avg5"
#puts "pair6 $avg6"
#puts "pair7 $avg7"
#puts "pair8 $avg8"
#
#puts "Average Throughput:	$avg Mbps"

puts "Save the test..."
set tstResult ${result}_$direct.tst
chrTest save $test $tstResult
set txtResult ${result}_$direct.txt
exec FMTTST $tstResult $txtResult

chrTest delete $test force
}
exit