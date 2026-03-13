# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # 3. Test Addition
    add_value = 10
    iterations = 5
    dut.ui_in.value = add_value

    dut._log.info(f"Adding {add_value} to accumulator {iterations} times")

    for i in range(1, iterations + 1):
        # 1. Drive the input
        dut.ui_in.value = add_value
        
        # 2. Wait for the edge where the hardware captures 'ui_in'
        await ClockCycles(dut.clk, 1)
        
        # 3. Read the result 
        # By waiting for a tiny 'ReadOnly' trigger or another cycle, we ensure we see the update.
        current_total = (int(dut.uio_out.value) << 8) | int(dut.uo_out.value)
        expected_total = add_value * i
        
        dut._log.info(f"Cycle {i}: Expected {expected_total}, Got {current_total}")
        assert current_total == expected_total

