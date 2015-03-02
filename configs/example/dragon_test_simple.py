#
# Author: Ankit More 
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

# Get paths we might need.  It's expected this file is in m5/configs/example.
config_path = os.path.dirname(os.path.abspath(__file__))
config_root = os.path.dirname(config_path)
m5_root = os.path.dirname(config_root)

parser = optparse.OptionParser()
Options.addCommonOptions(parser)

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

#
# Add the ruby specific and protocol specific options
#
Ruby.define_options(parser)
execfile(os.path.join(config_root, "common", "Options.py"))

(options, args) = parser.parse_args()

#
# Set the default cache size and associativity to be very small to encourage
# races between requests and writebacks.
#
#options.l1d_size="256B"
#options.l1i_size="256B"
#options.l2_size="512B"
#options.l3_size="1kB"
#options.l1d_assoc=2
#options.l1i_assoc=2
#options.l2_assoc=2
#options.l3_assoc=2

if args:
     print "Error: script doesn't take any positional arguments"
     sys.exit(1)

#
# Create the M5 system.  Note that the Memory Object isn't
# actually used by the tester, but is included to support the
# M5 memory size == Ruby memory size checks
#
system = System(physmem = SimpleMemory(in_addr_map = True, range=AddrRange(options.mem_size)))

#
# Create the dragon tester
#
system.tester = DragonTester(num_cpus = options.num_cpus, num_threads = options.num_threads, directory_shared_fraction = options.dir_shared_frac, deadlock_threshold = options.deadlock_threshold, eventDir = options.eventDir, outputDir = options.outputDir, skipLocal = options.skipLocalRW, masterWakeupFreq = options.masterFreq, cpi_iops = options.cpi_iops, cpi_flops = options.cpi_flops)


Ruby.create_system(options, system)

assert(options.num_cpus == len(system.ruby._cpu_ruby_ports))

for ruby_port in system.ruby._cpu_ruby_ports:
    #
    # Tie the ruby tester ports to the ruby cpu ports
    #
    system.tester.cpuPort = ruby_port.slave

# -----------------------
# run simulation
# -----------------------
system.debbie = 1
root = Root( full_system = False, system = system )
root.system.mem_mode = 'timing'

#Change garnet parameters for multiple runs - Sid
#system.ruby.network.vcs_per_vnet = options.vcs_per_vnet
#system.ruby.network.buffers_per_data_vc = options.buffers_per_data_vc
#system.ruby.network.ni_flit_size = options.bandwidth_factor
#print "hello:"+str(system.ruby.network.ni_flit_size)
for link in system.ruby.network.topology.int_links :
    #print link.bandwidth_factor
    link.bandwidth_factor = options.bandwidth_factor
    #print "hello:"+str(link.latency)
    #for link2 in link.nls:
        #print link2.channel_width
for link in system.ruby.network.topology.ext_links :
    #print link.bandwidth_factor
    link.bandwidth_factor = options.bandwidth_factor

# Not much point in this being higher than the L1 latency
m5.ticks.setGlobalFrequency('1ns')

# instantiate configuration
m5.instantiate()

# simulate until program terminates
exit_event = m5.simulate(options.maxtick)

print 'Exiting @ tick', m5.curTick(), 'because', exit_event.getCause()
