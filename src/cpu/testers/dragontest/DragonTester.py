# Karthik Sangaiah & Ankit More
#
# DragonTester.py 
# sets up the parameters that need to be provided to instantiate DragonTester
#

from MemObject import MemObject
from m5.params import *
from m5.proxy import *

class DragonTester(MemObject):
    type = 'DragonTester'
    #cxx_header = Param.String("cpu/testers/dragontest/DragonTester.hh")
    num_cpus = Param.Int("number of cpus / RubyPorts")
    num_threads = Param.Int("number of threads")
    directory_shared_fraction = Param.Int("shared fraction of the directory")
    cpuPort = VectorMasterPort("the cpu ports")
    #deadlock_threshold = Param.Int(50000, "how often to check for deadlock")
    deadlock_threshold = Param.Int(25000, "how often to check for deadlock")
    eventDir = Param.String("the location of the events profile")
    outputDir = Param.String("directory path to dump the output")
    skipLocal = Param.Bool("skip local R/W or not?")
    masterWakeupFreq = Param.Int(1000, "how often to wakeup the master event")
    cpi_iops = Param.Float(1, "CPI for integer ops")
    cpi_flops = Param.Float(2, "CPI for floating point ops")
    system = Param.System(Parent.any, "System we belong to")
