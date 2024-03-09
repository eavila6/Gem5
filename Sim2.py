"""
Authors: Carter Young and Ethan Avila
Date: 03/12/2024
Description: This file implements Simulation 2 as specified in the Project
2 Description for Professor Juan Flores' CS 422 Class (Flores, 2024).

To run: Go to terminal and enter ./build/X86/gem5.opt -d /home/carteryoung/gem5_output configs/example/Sim2.py --cpu-type=TimingSimpleCPU --caches --l1i_size=256kB --l1d_size=256kB --l1i_assoc=1 --l1d_assoc=1 --cacheline_size=32 --cmd=/gem5/Matrix/mat-mult

"""

from m5.objects import System, X86SimpleCPU, ArmSimpleCPU, SimpleMemory, Process
from m5.objects import Cache

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.cpu = TimingSimpleCPU()

l1i_size = '64kB'  # L1 Instruction Cache Size
l1d_size = '128kB' # L1 Data Cache Size
l2_size = '2MB'    # L2 Cache Size
associativities = [1, 2, 4, 8, 16, 32]

# L1 Instruction Cache
system.l1i_cache = Cache(size=l1i_size,
                         assoc=1,
                         cache_line_size=32,
                         writeback_clean=True,
                         tags=BaseSetAssoc())

# L1 Data Cache
system.l1d_cache = Cache(size=l1d_size,
                         assoc=1,
                         cache_line_size=32,
                         writeback_clean=True,
                         tags=BaseSetAssoc())

# L2 Cache (Shared)
system.l2_cache = Cache(size=l2_size,
                        assoc=assoc,  # Note: Adjust this if L2 associativity is to remain constant
                        cache_line_size=32,
                        writeback_clean=True,
                        tags=BaseSetAssoc())

# Connect the L1 caches to the CPU
system.cpu.icache_port = system.l1i_cache.cpu_side
system.cpu.dcache_port = system.l1d_cache.cpu_side

# Rest of system setup (e.g., memory system, bus)

# Example memory system setup
system.membus = SystemXBar()
system.l1i_cache.mem_side = system.membus.slave
system.l1d_cache.mem_side = system.membus.slave

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# Setup memory
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = ['/gem5/Matrix/mat-mult']
system.cpu.workload = process
system.cpu.createThreads()
