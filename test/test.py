# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import ClockCycles, ReadOnly


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
# 3. Test Addition
    add_value = 10
    iterations = 5
    
    # Drive the value BEFORE the loop starts
    dut.ui_in.value = add_value

    dut._log.info(f"Adding {add_value} to accumalator {iterations} times")

    for i in range(1, iterations + 1):
        # 1. Wait for the clock to trigger the hardware
        await ClockCycles(dut.clk, 1)
        
        # 2. Wait for a tiny amount of time for gates to settle 
        # (ReadOnly is good, but sometimes a small delay helps in GL)
        await ReadOnly() 
        
        # 3. Read the values
        # Use .integer to avoid issues with cocotb handles
        low_byte = dut.uo_out.value.integer
        high_byte = dut.uio_out.value.integer
        current_total = (high_byte << 8) | low_byte
        
        expected_total = add_value * i
    
        dut._log.info(f"Cycle {i}: Expected {expected_total}, Got {current_total}")
        assert current_total == expected_total
