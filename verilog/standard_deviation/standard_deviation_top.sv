module standard_deviation_top(

input logic clk,
input logic rstn,
input logic data_in,

output logic data_out

);


logic clk48;
logic clk20;


endmodule

module data_collector(

input logic clk,
input logic rstn,
input logic [32:0] epack,
input logic data_recieved,	//data has been collected by the standard_deviation module

output logic [15:0] pixel_packs [3392],
output logic data_sent		//lets the standard_deviation module know there is data ready

);

typedef enum { signal_wait, data_in, latch_data} states;
states state;

logic [15:0] chunck_data [3392];

logic [31:0] data_count; 	//counts to 16 so that data can be split into pixels 
logic [31:0] pixel_count;	//counts to 3392 so that all the data can be split into all 3392 pixels

always@(posedge clk or negedge rstn)
	begin
	case(state)
		signal_wait:
			begin
			
			end
		data_in:
			begin
			
			end
		latch_data:
			begin
			
			end
		default: state <= signal_wait;
	endcase
	end

endmodule


module standard_deviation(

input logic clk,
input logic rstn,
input logic data_sent,	//data ready to be collected
input logic [15:0] pixel_pack [3392],

output logic [15:0] sd_out,
output logic data_recieved	//data collected

);

typedef enum { data_wait, sum_data, calc, calc_sd} states;
states state;

logic [31:0] sum, vsum;
logic [31:0] mean, variance, sd;


always@(posedge clk)
	begin
		case(state)
			data_wait:
				begin
				
				end
			sum_data:
				begin
				
				end
			calc:
				begin
				
				end
			calc_sd:
				begin
				
				end
			default: state <= data_wait;
		endcase
	end

endmodule

module output_data(

input logic clk,
input logic rstn,

input logic [15:0] sd_data,

output logic [7:0] data_output_low,
output logic [7:0] data_output_high

);

typedef enum { output_wait, fill_outputs, send_data} states;
states state;

always@(posedge clk or negedge rstn)
	begin
		case(state)
			output_wait:
				begin
				
				end
			fill_outputs:
				begin
				
				end
			send_data:
				begin
				
				end
			default: state <= output_wait;
		endcase
	end

endmodule















