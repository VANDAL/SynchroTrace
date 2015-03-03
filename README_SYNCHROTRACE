SYNCHROTRACE:

There are two tools which together form the prototype SynchroTrace simulation flow built into Gem5.
	1) Sigil - Multi-threaded Trace Capture Tool
	2) Replay - Event-Trace Replay Framework
	
The logical steps to using this simulation environment for design space exploration or CMP simulation is as follows:
	1) Generate Multi-threaded Event Traces for the program binary you are testing (See Sigil documentation for further information):
		a) Use the Sigil wrapping script (runsigil_and_gz_newbranch.py) with necessary options on your binary
	2) Compile SynchroTrace
	3) Run SynchroTrace with necessary options on the generated traces
	
Simulating FFT with SynchroTrace (And generating traces):

1) Generate Traces for 8-threaded FFT (Options: -m16 -p8 -l6 -t):

a) /archgroup/archtools/postprocess_scripts/accel_select/runsigil_and_gz_newbranch.py --fair-sched=yes --tool=callgrind --separate-callers=100 --toggle-collect=main --cache-sim=yes --dump-line=no --drw-func=no --drw-events=yes --drw-splitcomp=1 --drw-intercepts=yes --drw-syscall=no --branch-sim=yes --separate-threads=yes --callgrind-out-file=callgrind.out.threads ./FFT -m16 -p8 -l6 -t

b) Generate Pthread synchronization metadata file (sigil.pthread.out) using the following script on err.gz which was generated when the traces are generated:

/archgroup/archtools/postprocess_scripts/noc_evaluation/generate_pthread_file.py err.gz

2) Compile SynchroTrace using SConscript:

cd synchrotrace
scons build/X86_MESI_CMP_directory/gem5.opt --jobs=6

3) Run SynchroTrace on the 8-thread traces of FFT:

./build/X86_MESI_CMP_directory/gem5.opt ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --topology=Mesh --mesh-rows=8 --eventDir=TRACEDIRECTORY --outputDir=OUTPUTDIRECTORY --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --cpi_iops=1 --cpi_flops=2 --bandwidth_factor=4 --l1_latency=3 --masterFreq=1 2> fft.err

where TRACEDIRECTORY is the path to the directory holding your generated traces and OUTPUTDIRECTORY is the path to your output directory.


Simulating FFT with SynchroTrace (Using Pre-generated Traces):

1) Compile SynchroTrace using SConscript:

scons build/X86_MESI_CMP_directory/gem5.opt --jobs=6

2) Run SynchroTrace on the 8-thread traces of FFT:

./build/X86_MESI_CMP_directory/gem5.opt ./configs/synchrotrace/synchrotrace.py --garnet-network=fixed --topology=Mesh --mesh-rows=8 --eventDir=TRACEDIRECTORY --outputDir=OUTPUTDIRECTORY --num-cpus=8 --num_threads=8 --num-dirs=8 --num-l2caches=8 --l1d_size=8kB --l1d_assoc=16 --l1i_size=8kB --l1i_assoc=2 --l2_size=128kB --l2_assoc=4 --cpi_iops=1 --cpi_flops=2 --bandwidth_factor=4 --l1_latency=3 --masterFreq=1 2> fft.err

where TRACEDIRECTORY is the path to the directory holding your generated traces and OUTPUTDIRECTORY is the path to your output directory.

Using Pre-generated traces:

We have included traces for various Splash2 and Parsec benchmarks (Using statically linked m5threads library) for at least 2/4/8/16/32 threads in /scratchlair/ks499-scratch/sigil_traces/

Sample 8-thread traces using the standard pthread library are located in /scratchlair/ks499-scratch/sigil_traces_std_pth_lib