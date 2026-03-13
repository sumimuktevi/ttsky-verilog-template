# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import ClockCycles, ReadOnly, FallingEdge, RisingEdge


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
    
    # Release reset on a FALLING edge so the 
    # hardware sees a stable '1' on the next rising edge
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Test Addition
    add_value = 10
    iterations = 5
    
    for i in range(1, iterations + 1):
        await FallingEdge(dut.clk)
        dut.ui_in.value = add_value
        
        await RisingEdge(dut.clk)
        await ReadOnly() # Wait for gate propagation
        
        # Check if values are 'X' before converting
        if dut.uo_out.value.is_resolvable:
            low_byte = dut.uo_out.value.to_unsigned()
            high_byte = dut.uio_out.value.to_unsigned()
            current_total = (high_byte << 8) | low_byte
            
            expected_total = add_value * i
            dut._log.info(f"Cycle {i}: Expected {expected_total}, Got {current_total}")
            assert current_total == expected_total
        else:
            # This will help you see the 'X' in the logs instead of crashing
            dut._log.error(f"Cycle {i}: Output is indeterminate! {dut.uo_out.value}")
            assert False
