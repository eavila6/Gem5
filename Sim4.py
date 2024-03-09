"""
Authors: Carter Young and Ethan Avila
Date: 03/12/2024
Description: This file implements a write-back cache class as specified in the Project
2 Description for Professor Juan Flores' CS 422 Class (Flores, 2024).

To run: Go to terminal and enter ./build/X86/gem5.opt -d /home/carteryoung/gem5_output configs/example/Sim1.py --cpu-type=TimingSimpleCPU --caches --l1i_size=256kB --l1d_size=256kB --l1i_assoc=1 --l1d_assoc=1 --cacheline_size=32 --cmd=/gem5/Matrix/mat-mult

"""

from m5.objects import *

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'  # Use 'timing' memory mode for detailed simulations
system.mem_ranges = [AddrRange('4GB')]  # Memory configuration

# CPU Setup
system.cpu = DerivO3CPU()
system.cpu.createThreads()

# L1 Instruction Cache
system.cpu.icache = Cache(size='64kB', assoc=2)
system.cpu.icache.cpu_side = system.cpu.icache_port

# L1 Data Cache
system.cpu.dcache = Cache(size='128kB', assoc=2)
system.cpu.dcache.cpu_side = system.cpu.dcache_port

# L2 Cache (Shared)
system.l2cache = Cache(size='2MB', assoc=4)
system.cpu.icache.mem_side = system.l2cache.cpu_side
system.cpu.dcache.mem_side = system.l2cache.cpu_side

# Connect L2 cache to the memory bus
system.l2bus = L2XBar()
system.l2cache.mem_side = system.l2bus.slave

# System Memory Bus
system.membus = SystemXBar()

# Connect the L2 bus to the main memory bus
system.l2bus.master = system.membus.slave

# Memory Controller Configuration
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Connect the system ports
system.system_port = system.membus.slave
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

process = Process()
process.cmd = ['/gem5/Matrix/mat-mult']
system.cpu.workload = process
system.cpu.createThreads()
