/*
 * Copyright (c) 1999-2012 Mark D. Hill and David A. Wood
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 * Contains all of the various parts of the system we are simulating.
 * Performs allocation, deallocation, and setup of all the major
 * components of the system
 */

#ifndef __MEM_RUBY_SYSTEM_SYSTEM_HH__
#define __MEM_RUBY_SYSTEM_SYSTEM_HH__

#include "base/callback.hh"
#include "mem/ruby/common/Global.hh"
#include "mem/ruby/eventqueue/RubyEventQueue.hh"
#include "mem/ruby/recorder/CacheRecorder.hh"
#include "mem/ruby/slicc_interface/AbstractController.hh"
#include "mem/ruby/system/MemoryVector.hh"
#include "mem/ruby/system/SparseMemory.hh"
#include "params/RubySystem.hh"
#include "sim/sim_object.hh"
//Added by Sid for capturing round trip time - Initialization
#include <vector>
#include "base/hashmap.hh"
//#include "gzstream.h"
#include <gzstream.hh>
struct threadStat {
  int ThreadID;
  unsigned long totalMemOps;
  unsigned long totalRTT;
  /*Added by Tianyun to print func name in RTT*/
  std::string func;
  /*Done addition by Tianyun*/
  threadStat() {  ThreadID = -1; totalRTT = 0; totalMemOps = 0; func="";}
  void clear() {  totalRTT = 0; totalMemOps = 0; }
};

class rttEventScheduler;
// class rttEventScheduler : public Consumer
// {
//   public:
//     rttEventScheduler()
//     {
//         g_eventQueue_ptr->scheduleEvent(this, 500);
//     }
//     void wakeup()
//     {
//         //Call outputEvents()
//         g_system_ptr->outputEvents();
//      //Put yourself back on the heap to be woken up
//      g_eventQueue_ptr->scheduleEvent(this, 500);
//      //Don't do anything special to go back to sleep
//     }
// };
//Done additions by Sid


class Network;
class Profiler;

class RubySystem : public SimObject
{
  public:
    class RubyEvent : public Event
    {
      public:
        RubyEvent(RubySystem* _ruby_system)
        {
            ruby_system = _ruby_system;
        }
      private:
        void process();

        RubySystem* ruby_system;
    };

    friend class RubyEvent;

    typedef RubySystemParams Params;
    RubySystem(const Params *p);
    ~RubySystem();

    // config accessors
    static int getRandomSeed() { return m_random_seed; }
    static int getRandomization() { return m_randomization; }
    static int getBlockSizeBytes() { return m_block_size_bytes; }
    static int getBlockSizeBits() { return m_block_size_bits; }
    static uint64 getMemorySizeBytes() { return m_memory_size_bytes; }
    static int getMemorySizeBits() { return m_memory_size_bits; }

    // Public Methods
    static Network*
    getNetwork()
    {
        assert(m_network_ptr != NULL);
        return m_network_ptr;
    }

    static RubyEventQueue*
    getEventQueue()
    {
        return g_eventQueue_ptr;
    }

    Profiler*
    getProfiler()
    {
        assert(m_profiler_ptr != NULL);
        return m_profiler_ptr;
    }

    static MemoryVector*
    getMemoryVector()
    {
        assert(m_mem_vec_ptr != NULL);
        return m_mem_vec_ptr;
    }

    static void printConfig(std::ostream& out);
    static void printStats(std::ostream& out);
    void clearStats() const;

    uint64 getInstructionCount(int thread) { return 1; }
    static uint64
    getCycleCount(int thread)
    {
        return g_eventQueue_ptr->getTime();
    }

    void print(std::ostream& out) const;

    void serialize(std::ostream &os);
    void unserialize(Checkpoint *cp, const std::string &section);
    void process();
    void startup();

    void registerNetwork(Network*);
    void registerProfiler(Profiler*);
    void registerAbstractController(AbstractController*);
    void registerSparseMemory(SparseMemory*);

    bool eventQueueEmpty() { return eventq->empty(); }
    void enqueueRubyEvent(Tick tick)
    {
        RubyEvent* e = new RubyEvent(this);
        schedule(e, tick);
    }

    int num_simulated_threads;
    std::vector<unsigned long> totalRead;
    std::vector<unsigned long> totalReadBytes;
    std::vector<unsigned long> totalWrite;
    std::vector<unsigned long> totalWriteBytes;
    //Paco (8/20) - Added to capture memory traffic per barrier

    std::vector<unsigned long> totalRead_per_barrier;
    std::vector<unsigned long> totalReadBytes_per_barrier;
    std::vector<unsigned long> totalWrite_per_barrier;
    std::vector<unsigned long> totalWriteBytes_per_barrier;

    std::vector<unsigned long> thread_cycles_per_event;

    int num_barrier; // Current Barrier #
    int num_flits_per_barrier; // Total number of flits generated in Barrier
    double accumulated_queue_delay_per_barrier; // Paco (9/16)
    double accumulated_network_latency_per_barrier; // Paco (9/16)
    double packets_per_barrier; // Paco (9/16)
    double previous_barrier_cycle_time; // Paco (9/16)
    double previous_router_energy; // Paco (9/16)
    std::vector<unsigned int> l1cacheMiss_per_barrier;
    double accumulated_queue_delay_per_net_wakeup; // Paco (11/13)
    double accumulated_network_latency_per_net_wakeup; // Paco (11/13)
    double packets_per_net_wakeup; // Paco (11/13)
    int ni_wakeup_counter; // Paco (11/13)

    // Paco (12/1) - Must log flits injected in and flits removed. Moving average over 500 cycle intervals. Find the spots where we inject packets and remove packets in NetworkInterface_d.cc
    int flits_in_flight;
    double flits_in_flight_accum;
    double flits_in_flight_prev_cycle;

    void printMemoryEventsInBarrier(); // Prints and Clears memory events in a barrier

    //Added by Sid for capturing round trip time
    std::vector< m5::hash_map<int, int> > roundTripTime;
    std::vector<int> maxRTT;    //RTT --> rount trip time
    std::vector<unsigned long> totalRTT;
    std::vector<int> lastMsgTriggerTime;
    void outputRTT_hist();
    std::vector<ogzstream *> outputFilePointer;
    std::vector<threadStat> threadStatistics;
    void rtt_init();
    bool rtt_init_flag;
    // called when the timer hits for outputting the event files
    void outputEvents();
    //For when we initialize rttEventScheduler
    rttEventScheduler *rtt_eventscheduler_ptr;
    //Done additions by Sid

  private:
    // Private copy constructor and assignment operator
    RubySystem(const RubySystem& obj);
    RubySystem& operator=(const RubySystem& obj);

    void init();

    static void printSystemConfig(std::ostream& out);
    void readCompressedTrace(std::string filename,
                             uint8*& raw_data,
                             uint64& uncompressed_trace_size);
    void writeCompressedTrace(uint8* raw_data, std::string file,
                              uint64 uncompressed_trace_size);

  private:
    // configuration parameters
    static int m_random_seed;
    static bool m_randomization;
    static Tick m_clock;
    static int m_block_size_bytes;
    static int m_block_size_bits;
    static uint64 m_memory_size_bytes;
    static int m_memory_size_bits;
    static Network* m_network_ptr;

  public:
    static Profiler* m_profiler_ptr;
    static MemoryVector* m_mem_vec_ptr;
    std::vector<AbstractController*> m_abs_cntrl_vec;
    bool m_warmup_enabled;
    bool m_cooldown_enabled;
    CacheRecorder* m_cache_recorder;
    std::vector<SparseMemory*> m_sparse_memory_vector;
};

inline std::ostream&
operator<<(std::ostream& out, const RubySystem& obj)
{
    //obj.print(out);
    out << std::flush;
    return out;
}

class RubyExitCallback : public Callback
{
  private:
    std::string stats_filename;

  public:
    virtual ~RubyExitCallback() {}

    RubyExitCallback(const std::string& _stats_filename)
    {
        stats_filename = _stats_filename;
    }

    virtual void process();
};

//Added by Sid for capturing round trip time - Initialization
class rttEventScheduler : public Consumer
{
  public:
    rttEventScheduler();
    void wakeup();
    void print(std::ostream& out) const;
  //void storeEventInfo(int info);
};
//Done additions by Sid

#endif // __MEM_RUBY_SYSTEM_SYSTEM_HH__
