SYNCHROTRACE:

There are two tools which together form the prototype SynchroTrace simulation flow built into Gem5.
	1) Sigil - Multi-threaded Trace Capture Tool
	2) Replay - Event-Trace Replay Framework

This code base includes (2) Replay. 
Currently, the Sigil version required to generate traces is provided separately from the same github user "dpac-vlsi".
	
The logical steps to using this simulation environment for design space exploration or CMP simulation is as follows:
	1)
	  a) Generate Multi-threaded Event Traces for the program binary you are testing (See Sigil documentation for further information):
		-Use the Sigil wrapping script (runsigil_and_gz_newbranch.py) with necessary options on your binary
	   OR
	  b) Use previously generated or sample traces
	2) Compile SynchroTrace (For a list of dependencies, please look in the Additional Notes section below)
	3) Run SynchroTrace with necessary options on the generated traces
	
Simulating FFT with SynchroTrace (Using Pre-generated Traces):

1) Compile SynchroTrace using SConscript:

  a) Go to the base SynchroTrace directory
  b) Run the following command (Note that the number of jobs refers to the number of cores available for compilation):
     
     scons build/X86_MESI_CMP_directory/gem5.opt --jobs=6

2) Run SynchroTrace on the 8-thread traces of FFT:

  a) Go to the base SynchroTrace directory
  b) Run the following script:

  run_synchrotrace_fft.pl

######## Steps to build and run FFT example

```sh
$ git clone https://github.com/dpac-vlsi/SynchroTrace
$ cd SynchroTrace
$ python -V
$ scons --version
```
Python 2.7.6 or above and scons 2.3.0 or above is required to run build and run SynchroTrace.
For more information on requirements, check 5) in the additional notes below.
Currently we do not provide any means to automatically check dependencies and install the missing packages.

```sh
$ scons build/X86_MESI_CMP_directory/gem5.opt --jobs=6
```
At this point, the gem5 executable should be built with integrated Replay in the location specified in the command above.
gem5 is usually run with a configuration script that hooks up the various architecture models packaged with the gem5 framework.
We have written a SynchroTrace configuration script to which arguments can be passed to configure the desired system.
This script can be found at <SYNCHROTRACE_FOLDER>/configs/synchrotrace/synchrotrace.py

The run_synchrotrace_fft.pl run script can be used to run the FFT example simply as follows:

```sh
$ ./run_synchrotrace_fft.pl
```

This script can be modified and emulated to run your own configuration.
A different trace location by changing the $eventDir variable.
This design being simulated is set by changing the arguments provided in the $synchrotracecmd variable.
For a list of valid arguments, run the following from the main SynchroTrace folder:

```sh
$ ./build/X86_MESI_CMP_directory/gem5.opt ./configs/synchrotrace/synchrotrace.py --help
```

####################################################################################################################################
Additional Notes:

1) Sample Sigil Traces are located in $BASESYNCHROTRACEDIR/sample_sigil_traces

2) SynchroTrace configurations are located in $BASESYNCHROTRACEDIR/configs/synchrotrace/synchrotrace.py and $BASESYNCHROTRACEDIR/configs/ruby/Ruby.py

3) The run_synchrotrace_fft.pl run script has a section for debug flags. The following is a list of the available debug flags used by SynchroTrace with brief descriptions.

DebugFlag('mutexLogger') - Prints order of threads obtaining mutex lock
DebugFlag('printEvent') - Prints EventID# for specific thread before/after event started/completed. This debug flag makes the simulation time very slow.
DebugFlag('printEventFull') - Prints EventIDs for Threads, Threads on what Cores every 50k cycles
DebugFlag('cacheMiss') - Prints out cache misses as they happen and address 
DebugFlag('memoryInBarrier') - prints memory reads, writes, read bytes, write bytes every barrier
DebugFlag('flitsInBarrier') - prints flits generated every barrier
DebugFlag('l1MissesInBarrier') - prints l1 misses per thread every barrier
DebugFlag('latencyInBarrier') - prints 3 lines. # packets in barrier, Accumulated queueing delay in barrier, Accumulated network latency in Barrier.
DebugFlag('powerStatsInBarrier') - prints the total router power specifically for that barrier, i.e. not a rolling average.
DebugFlag('roi') - Prints out the cycle when we reach the parallel region in Debate. Prints out when the threads all join up.
DebugFlag('netMessages') - Prints the network packet messages out at 10k cycle buckets.
DebugFlag('amTrace') - Original default debug flag.

4) An example of this command with a debug flag is as follows:
./build/X86_MESI_CMP_directory/gem5.opt --debug-flags=printEventFull ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --topology=Mesh --mesh-rows=8 --eventDir=$eventDir --outputDir=$outputDir --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --cpi_iops=1 --cpi_flops=2 --bandwidth_factor=4 --l1_latency=3 --masterFreq=1 2> fft.err";

where the $eventDir points to the directory of the traces and $outputDir points to the desired output directory path.

5) Necessary Dependencies:
   gcc-4.4.7
   gmp-5.1.1
   mpc-1.0
   mpfr-3.1.2
   swig-2.0.1
   python-2.7.6
   scons-2.3.0