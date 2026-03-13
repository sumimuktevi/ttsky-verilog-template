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
        await ClockCycles(dut.clk, 1)
        //await ClockCycles(dut.clk, 1) 
        
        # Combine uio_out (high byte) and uo_out (low byte) to get 16-bit total
        current_total = (int(dut.uio_out.value) << 8) | int(dut.uo_out.value)
        expected_total = add_value * i
        
        dut._log.info(f"Cycle {i}: Expected {expected_total}, Got {current_total}")
        assert current_total == expected_total

    # 4. Test Big Value
    dut.ui_in.value = 255 
    await ClockCycles(dut.clk, 10) 
    
    final_total = (int(dut.uio_out.value) << 8) | int(dut.uo_out.value)
    dut._log.info(f"Final Total after large additions: {final_total}")
    
    # Checks that top bits are being used
    assert int(dut.uio_out.value) > 0
    dut._log.info("Tests passed")


