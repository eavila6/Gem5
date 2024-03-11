"""
Authors: Carter Young and Ethan Avila
Date: 03/12/2024
Description: This file implements a write-back cache class as specified in the Project
2 Description for Professor Juan Flores' CS 422 Class (Flores, 2024).

To run:
1. Relocate Sim{#}.py in any gem5 directory
2. Create output directory for results
3. Navigate to gem5 directory in terminal
4. In terminal, enter "./build/X86/gem5.opt -d <output_filepath> <sim#.py_filepath>
"""

import m5
from m5.objects import *
from m5.util import convert
from caches import *

# Create the system
system = System()

# Set system clock frequency
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up system as specified
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('4GB')]
system.membus = SystemXBar()

# Create a CPU
system.cpu = TimingSimpleCPU()

# L1 Instruction Cache
system.cpu.icache = L1ICache(
    size='64kB',  # Change for study
    assoc=2,  # 2-way set-associative
    tag_latency=1,  # Set L1 hit time
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20,
    writeback_clean=True,
    tags=BaseSetAssoc()
)

# L1 Data Cache
system.cpu.dcache = L1DCache(
    size='256kB',  # Change for study
    assoc=2,  # 2-way set-associative
    tag_latency=1,  # Set L1 hit time
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20,
    writeback_clean=True,
    tags=BaseSetAssoc()
)

# L2 Cache
system.l2cache = L2Cache(
    size='8MB',  # Change for study
    assoc=4,  # 4-way set-associative
    tag_latency=10,  # Set L2 hit time
    data_latency=10,  # Assuming data latency follows tag latency for L2
    response_latency=10,  # Assuming response latency follows tag latency for L2
    mshrs=4,
    tgts_per_mshr=20,
    writeback_clean=True,
    tags=BaseSetAssoc()
)

# Intermediary bus between L1 caches and L2 cache
system.l2bus = L2XBar()

# Connecting the caches
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# Memory controller configuration
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Processor interrupts configuration
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Binary and workload configuration
# binary = '/home/carteryoung/gem5/configs/example/mat-mult'  # Adjust this path
#Ethan's bin path
binary = '/home/ethan429/Documents/CS429/Gem5/mat-mult'  # adjust as needed

system.workload = SEWorkload.init_compatible(binary)
process = Process()
# fyi you gotta manually type in matrix params via terminal
# bc of the way  mat-mult is set up & gem5 being weird
# args in the form of 100 100\n100 100 or 100\n100\n100\n100inputted from terminal
process.cmd = [binary, 100]  # Assuming '100' is an argument to your binary
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate and run
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %s because %s' % (exit_event.getCause(), m5.curTick()))
