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
# SynchroTrace.py
#
# Sets up the parameters to instantiate SynchroTrace
#

from MemObject import MemObject
from m5.params import *
from m5.proxy import *

class SynchroTrace(MemObject):
    type = 'SynchroTrace'
    num_cpus = Param.Int("number of cpus / RubyPorts")
    num_threads = Param.Int("number of threads")
    directory_shared_fraction = Param.Int("shared fraction of the directory")
    cpuPort = VectorMasterPort("the cpu ports")
    deadlock_threshold = Param.Int(25000, "how often to check for deadlock")
    eventDir = Param.String("the location of the events profile")
    outputDir = Param.String("directory path to dump the output")
    skipLocal = Param.Bool("skip local R/W or not?")
    masterWakeupFreq = Param.Int(1, "how often to wakeup the master event")
    cpi_iops = Param.Float(1, "CPI for integer ops")
    cpi_flops = Param.Float(2, "CPI for floating point ops")
    system = Param.System(Parent.any, "System we belong to")
