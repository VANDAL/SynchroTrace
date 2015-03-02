# Copyright (c) 2009-2011 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Brad Beckmann

#
# Full system configuraiton for ruby
#

import optparse
import sys

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal

addToPath('../common')
addToPath('../ruby')

import Ruby

from FSConfig import *
from SysPaths import *
from Benchmarks import *
import Options
import Simulation

def addExternalDisk(cur_sys):
     cur_sys.cf1 = CowIdeDisk(driveID='master')
     cur_sys.cf1.childImage(disk("benchmarks.img"))
     # default to an IDE controller rather than a CF one
     # assuming we've got one
     try:
         cur_sys.realview.ide.disks = [cur_sys.cf0, cur_sys.cf1]
     except:
         cur_sys.realview.cf_ctrl.disks = [cur_sys.cf0, cur_sys.cf1]

     return cur_sys
parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addFSOptions(parser)

# Add the ruby specific and protocol specific options
Ruby.define_options(parser)

(options, args) = parser.parse_args()
options.ruby = True

if args:
    print "Error: script doesn't take any positional arguments"
    sys.exit(1)

if options.benchmark:
    try:
        bm = Benchmarks[options.benchmark]
    except KeyError:
        print "Error benchmark %s has not been defined." % options.benchmark
        print "Valid benchmarks are: %s" % DefinedBenchmarks
        sys.exit(1)
else:
    bm = [SysConfig(disk=options.disk_image, mem=options.mem_size)]

# Check for timing mode because ruby does not support atomic accesses
if not (options.cpu_type == "detailed" or options.cpu_type == "timing"):
    print >> sys.stderr, "Ruby requires TimingSimpleCPU or O3CPU!!"
    sys.exit(1)
(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)

CPUClass.clock = options.clock

if buildEnv['TARGET_ISA'] == "alpha":
    system = makeLinuxAlphaRubySystem(test_mem_mode, bm[0])
elif buildEnv['TARGET_ISA'] == "x86":
    system = makeLinuxX86System(test_mem_mode, options.num_cpus, bm[0], True)
    #system = addExternalDisk(system)
    Simulation.setWorkCountOptions(system, options)
else:
    fatal("incapable of building non-alpha or non-x86 full system!")
if options.mem_size:
    bm[0]=SysConfig(disk=bm[0].disk, mem=options.mem_size,script=bm[0].script())
if options.kernel is not None:
    system.kernel = binary(options.kernel)

if options.script is not None:
    system.readfile = options.script

#Added by Tianyun for adding bm binary path to command line
if options.obj is None:
	print "Please specify the benchmark binary";
	sys.exit(1)
else:
	system.obj = options.obj
#Done addition by Tianyun

#Added by Tianyun for identifying debbie run from gem5 run
#if options.debbie is None:
#	print "Please sepcify debbie option"
#	sys.exit(1)
#else:
system.debbie = 0 #options.debbie
#Done addtion by Tianyun
system.cpu = [CPUClass(cpu_id=i) for i in xrange(options.num_cpus)]
Ruby.create_system(options, system, system.piobus, system._dma_ports)

for (i, cpu) in enumerate(system.cpu):
    #
    # Tie the cpu ports to the correct ruby system ports
    #
    cpu.createInterruptController()
    cpu.icache_port = system.ruby._cpu_ruby_ports[i].slave
    cpu.dcache_port = system.ruby._cpu_ruby_ports[i].slave
    if buildEnv['TARGET_ISA'] == "x86":
        cpu.itb.walker.port = system.ruby._cpu_ruby_ports[i].slave
        cpu.dtb.walker.port = system.ruby._cpu_ruby_ports[i].slave
        cpu.interrupts.pio = system.piobus.master
        cpu.interrupts.int_master = system.piobus.slave
        cpu.interrupts.int_slave = system.piobus.master

root = Root(full_system = True, system = system)
Simulation.run(options, root, system, FutureClass)
