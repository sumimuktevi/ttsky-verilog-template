/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs; Input A
    output wire [7:0] uo_out,   // Dedicated outputs; Sum (Lower bits)
    input  wire [7:0] uio_in,   // IOs: Input path; Iunused
    output wire [7:0] uio_out,  // IOs: Output path;  Sum (Higher bits)
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  //assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  //assign uio_out = 0;
  assign uio_oe  = 8'b1111_1111; // all of them are outputs because we need the higher bits of the accumalator  

    reg [15:0] accumalator; 
    assign uo_out  = accumalator[7:0];
    assign uio_out = accumalator[15:8];
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin 
            accumalator <= 16'd0;
        end else if (ena) begin 
            accumalator <= {8'b0,ui_in} + accumalator;
        end 
    end 
        
  // List all unused inputs to prevent warnings
    wire _unused = &{uio_in, 1'b0};

endmodule
