`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Replace tt_um_example with your module name:
  tt_um_example user_project (
     /*.clk(clk),
     .rst_n(rst_n),
     .ena(ena);
     .ui_in(ui_in);
     .uio_in(uio_in);
     .uo_out(uo_out);
     .uio_out(uio_out);
     .uio_oe(uio_oe);*/
      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );

   //Clock
  always #50 clk = ~clk;

  initial begin
    // Initializes signals
    clk = 0;
    rst_n = 0;
    ena = 0;
    ui_in = 0;
    uio_in = 0;

    // Reset 
    #100;
    rst_n = 1;
    #100;
    ena = 1;      // Enable the design

    // Test 1: Addition
    // Adds 10 to the accumulator
    ui_in = 8'd10; 
    #100;
     
    // Test Case 2: Accumulate 5 several times
    ui_in = 8'd5;
    repeat (4) #100; // Adds 5, four times (Total should be 10 + 20 = 30)

    // Test Case 3: carries bit over
     // 30 + 230 = 260
    ui_in = 8'd230;
    #100;

    // Test Case 4: Observe uio_out (High Byte)
    // Add 255 ten times to see the high byte increment quickly
    ui_in = 8'd255;
    repeat (10) #100;

    #100;
    $display("Test Finished. Final Sum (Hex): %h%h", uio_out, uo_out);
    $finish;
  end

endmodule
