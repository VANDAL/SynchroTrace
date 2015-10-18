#!/usr/bin/perl -w

#Assign your event and output directories
use Cwd;
my $eventDir=cwd()."/sample_sigil_traces/sigil_splitby1/fft/simsmall/8";
my $outputDir=".";

#Sample Debug command (Be sure to compile gem5.debug instead of gem5.opt prior to running this debug command)
my $gdbcmd="gdb --args ./build/X86_MESI_CMP_directory/gem5.debug ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --eventDir=$eventDir --outputDir=$outputDir --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --masterFreq=1 2> fft.err";

#Main run command
my $synchrotracecmd="./build/X86_MESI_CMP_directory/gem5.opt --debug-flags=printEventFull ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --topology=Mesh --mesh-rows=8 --eventDir=$eventDir --outputDir=$outputDir --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --cpi_iops=1 --cpi_flops=2 --bandwidth_factor=4 --l1_latency=3 --masterFreq=1 2> fft.err";

#--debug-flags=printEvent,printEventFull,mutexLogger,cacheMiss,memoryInBarrier,flitsInBarrier,l1MissesInBarrier,latencyInBarrier,powerStatsInBarrier,netMessages,roi

#system($gdbcmd);
system($synchrotracecmd);
