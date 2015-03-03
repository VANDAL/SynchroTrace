#Copyright (c) 2015, Drexel University
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Authors: Karthik Sangaiah & Ankit More
#
# synchrotrace.py
#
# Instantiate SynchroTrace
#
#
# Authors: Karthik Sangaiah & Ankit More 
#

import m5
from m5.objects import *
from m5.defines import buildEnv
from m5.util import addToPath
import os, optparse, sys
addToPath('../common')
addToPath('../ruby')
addToPath('../topologies')

import Options
import Ruby

# Get Relevant Paths
config_path = os.path.dirname(os.path.abspath(__file__))
config_root = os.path.dirname(config_path)

# Add Gem5 Options
parser = optparse.OptionParser()
Options.addCommonOptions(parser)

# SynchroTrace Specific Options
parser.add_option("--num_cpus", type="int", default=4, help="Number of cpus")
parser.add_option("--num_threads", type="int", default=4, help="Number of threads")
parser.add_option("--dir_shared_frac", type="int", default=2, help="Fraction of the directory used as shared memory (eg. 1/2->2)")
parser.add_option("--deadlock_threshold", metavar="N", default=50000, help = "Number of cycles to wait before declaring deadlock")
parser.add_option("--skipLocalRW", type="int", default=False, help="Skip local reads and writes?")
parser.add_option("--eventDir", type="string", default="", help="path to the directory that contains the event traces")
parser.add_option("--outputDir", type="string", default="", help="path to the directory where to dump the output")
parser.add_option("--masterFreq", type="int", default=1000, help="Frequency at which to wake up master event")
parser.add_option("--cpi_iops", type="float", default=1, help="CPI for integer ops")
parser.add_option("--cpi_flops", type="float", default=1, help="CPI for floating point ops")
parser.add_option("--buffers_per_data_vc", type="int", default=4, help="Buffer Depth per Virtual Channel")
parser.add_option("--vcs_per_vnet", type="int", default=4, help="Number of Virtual Channels per Network")
parser.add_option("--bandwidth_factor", type="int", default=16, help="Number of Virtual Channels per Network")
parser.add_option("--mem-size", action="store", type="string", default="1024MB", help="Memory Size physical memory(with unit. E.g. 512MB)")
parser.add_option("--l1_latency", action="store", type="int", default="3", help="Latency of a L1 Hit")

# Add the ruby specific and protocol specific options
Ruby.define_options(parser)
execfile(os.path.join(config_root, "common", "Options.py"))
(options, args) = parser.parse_args()

if args:
     print "Error: script doesn't take any positional arguments"
     sys.exit(1)

# Create the M5 System
system = System(physmem = SimpleMemory(in_addr_map = True, range=AddrRange(options.mem_size)))

# Create the SynchroTrace Replay Mechanism
system.tester = SynchroTrace(num_cpus = options.num_cpus, num_threads = options.num_threads, directory_shared_fraction = options.dir_shared_frac, deadlock_threshold = options.deadlock_threshold, eventDir = options.eventDir, outputDir = options.outputDir, skipLocal = options.skipLocalRW, masterWakeupFreq = options.masterFreq, cpi_iops = options.cpi_iops, cpi_flops = options.cpi_flops)

# Create the Ruby Instance
Ruby.create_system(options, system)

# Tie the SynchroTrace ports to the ruby cpu ports
assert(options.num_cpus == len(system.ruby._cpu_ruby_ports))
for ruby_port in system.ruby._cpu_ruby_ports:
    system.tester.cpuPort = ruby_port.slave
# Use SynchroTrace Options for Garnet Parameters
system.ruby.network.vcs_per_vnet = options.vcs_per_vnet
system.ruby.network.buffers_per_data_vc = options.buffers_per_data_vc
system.ruby.network.ni_flit_size = options.bandwidth_factor
for link in system.ruby.network.topology.int_links :
    link.bandwidth_factor = options.bandwidth_factor
for link in system.ruby.network.topology.ext_links :
    link.bandwidth_factor = options.bandwidth_factor


# Setup simulation
system.synchrotrace = 1
root = Root( full_system = False, system = system )
root.system.mem_mode = 'timing'

# Not much point in this being higher than the L1 latency
m5.ticks.setGlobalFrequency('1ns')

# instantiate configuration
m5.instantiate()

# simulate until program terminates
exit_event = m5.simulate(options.maxtick)

print 'Exiting @ tick', m5.curTick(), 'because', exit_event.getCause()
