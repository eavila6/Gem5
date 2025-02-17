"""
Authors: Carter Young and Ethan Avila
Date: 03/12/2024
Description: This file implements an x86 write-back cache class as specified in the Project
2 Description for Professor Juan Flores' CS 422 Class (Flores, 2024).

To run:
1. Relocate Sim{#}.py in any gem5 directory
2. Create output directory for results
3. Navigate to gem5 directory in terminal
4. In terminal, enter "./build/X86/gem5.opt -d <output_filepath> <sim#.py_filepath>
example: /build/X86/gem5.opt  -d /home/ethan429/Documents/CS429/m5out /home/ethan429/Documents/CS429/Gem5/Sim1.py

FYI for anyone else hoping to run this prog, you'll need to change the binary path,
as described in the binary section of this code
"""

# import the m5 lib
import m5
# import SimObjects we want
from m5.defines import buildEnv
from m5.objects import *
from m5.util import convert

from caches import *

# create the system we'll sim
system = System()

# set system clock freq (for parent & children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# set up system
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('4GB')]
system.membus = SystemXBar()

# create a simple CPU
system.cpu = AtomicSimpleCPU()  # Use ArmSimpleCPU() for ARM

# L1 Instruction Cache
system.cpu.icache = L1ICache(size='256kB',
                         assoc=32,
                         tag_latency=20,
                         data_latency=2,
                         response_latency = 2,
                         mshrs = 4,
                         tgts_per_mshr = 20,
                         writeback_clean=True,
                         tags=BaseSetAssoc())

# L1 Data Cache
system.cpu.dcache = L1DCache(size='256kB',
                         assoc=32,
                         tag_latency=20,
                         data_latency=2,
                         response_latency = 2,
                         mshrs = 4,
                         tgts_per_mshr = 20,
                         writeback_clean=True,
                         tags=BaseSetAssoc())


# Connect the L1 caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# create mem bus
system.membus=SystemXBar()

# connect caches to bus
system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)

# Processor interrupts
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory controller configuration
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]

# Connect mem to cpu
system.mem_ctrl.port = system.membus.mem_side_ports

#binary = '/home/carteryoung/mat-mult'  # Make sure to adjust this path
#Ethan's bin path
binary = '/home/ethan429/Documents/CS429/Gem5/mat-mult'  # adjust as needed

# Workload and process configuration
system.workload = SEWorkload.init_compatible(binary)

# create a process for our binary
process = Process()

#  print("waiting for command")
# set the command
process.cmd = [binary, 100,100,100,100]
# print("after binary command")

# set up the CPU to work and gen threads
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate and run
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print(f'Exiting @ tick {m5.curTick()}  because {exit_event.getCause()}')
# print('Exiting @ tick {} because {}' % (m5.curTick(), exit_event.getCause()))
