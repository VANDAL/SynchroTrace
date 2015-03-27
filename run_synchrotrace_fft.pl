#!/usr/bin/perl -w

use Cwd;
my $eventDir=cwd()."/sample_sigil_traces/sigil_splitby1/fft/simsmall/8";
my $outputDir=".";

my $gdbcmd="gdb --args ./build/X86_MESI_CMP_directory/gem5.debug ./configs/example/synchrotrace.py --garnet-network=fixed --eventDir=$eventDir --outputDir=$outputDir --num-cpus=8 --num_threads=8 --num-dirs=4 --num-l2caches=8 --l1d_size=64kB --l1d_assoc=4 --l1i_size=64kB --l1i_assoc=4 --l2_size=4096kB --l2_assoc=8 --vcs_per_vnet=4 --bandwidth_factor=4 --masterFreq=10000 2> fft.err";

my $pthreadcmd="./build/X86_MESI_CMP_directory/gem5.opt ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --topology=Mesh --mesh-rows=8 --eventDir=$eventDir --outputDir=$outputDir --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --cpi_iops=1 --cpi_flops=2 --bandwidth_factor=4 --l1_latency=3 --masterFreq=1 2> fft.err";

#--debug-flags=printEvent,printEventFull,mutexLogger,cacheMiss,memoryInBarrier,flitsInBarrier,l1MissesInBarrier,latencyInBarrier,powerStatsInBarrier,netMessages,roi

#system($gdbcmd);
system($pthreadcmd);
