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

input logic 				clk,
input logic 				rstn,
input logic 	[32:0] 	epack,
input logic 				data_recieved,	//data has been collected by the standard_deviation module
input logic					data_complete, //comes from standard dev

output logic 	[15:0] 	pixel_packs [3392],
output logic				data_ready //lets the standard_deviation module know there is data ready

);

typedef enum { signal_wait, data_in, latch_data} states;
states 						state;

logic [15:0] 				chunck_data [3392];

logic [31:0] 				data_count; 	//counts to 16 so that data can be split into pixels 
logic [31:0] 				pixel_count;	//counts to 3392 so that all the data can be split into all 3392 pixels

always@(posedge clk or negedge rstn)
	begin
		if(rstn == 'b0)
			begin
			pixel_packs 		<= '{default:'b0};
			data_ready 			<= 'b0;
			state 				<= signal_wait;
			chunck_data 		<= '{default:'b0};
			data_count 			<= 'd0;
			pixel_count 		<= 'd0;
			end
		else
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
						if(data_complete == 'b0) //make sure the last data set is done
							begin
							pixel_packs <= chunck_data;
							data_ready <= 'b1;
							end
						else
							begin
							state <= latch_data;
							end
						end
					default: state <= signal_wait;
				endcase
			end
	end

endmodule


module standard_deviation(

input logic 				clk,
input logic 				rstn,
input logic 				data_ready,	//data ready to be collected
input logic					data_sent, //data is sent to the PC
input logic 	[15:0] 	pixel_pack [3392],

output logic 	[15:0] 	sd_out,
output logic 				data_recieved,	//data collected
output logic				data_complete	//goes to data collector

);

typedef enum { data_wait, sum_data, calc, calc_sd} states;
states 					state;
typedef enum { send, hold, received} sending_states;
sending_states			sending_state;

logic [31:0] 			sum, vsum;
logic [31:0] 			mean, variance, sd;
logic [31:0]			sum_count;
logic [15:0]			x;
logic [31:0]			sqrt_out;
logic [31:0]			sqrt_count;

sqrt	sqrt_inst (
	.clock ( clk ),
	.data ( variance ),
	.result ( sqrt_out )
	);
	
	
always@(posedge clk)
	begin
		if(rstn == 'b0)
			begin
				sd_out 			<= 'd0;
				data_recieved 	<= 'b0;
				sum 				<= 'd0;
				vsum 				<= 'd0;
				mean 				<= 'd0;
				variance 		<= 'd0;
				sd 				<= 'd0;
				sum_count		<= 'd0;
				state				<= data_wait;
				sending_state	<= send;
			end
		else
			begin
				case(state)
					data_wait:
						begin
						if(!data_ready)
							begin
							state <= data_wait;
							end
						else
							begin
							state <= sum_data;
							end
						end
					sum_data:
						begin
						if(sum_count == 'd3392)
							begin
							sum_count <= 'd0;
							state <= calc;
							end
						else
							begin
							x <= pixel_pack[sum_count];
							sum += x;
							vsum += (x * x);
							sum_count++;
							state <= sum_data;
							end
						end
					calc:
						begin
						mean <= sum / 'd3392;
						variance <= vsum / 'd3392;
						state <= calc_sd;
						end
					calc_sd:
						begin
						if(sqrt_count >= 'd28) //wait for the sqrt module to compute the value of sd
							begin
							sqrt_count <= 'd0;
							sd <= sqrt_out;
							//send a start signal to ethernet send module
							state <= data_wait;
							end
						else
							begin
							sqrt_count++;
							state <= calc_sd;
							end
						end
					send_data:
						begin
							case(sending_state)
								send:
									begin
									sd_out <= sd;
									//could put mean here
									//could put variance here
									sending_state <= hold;
									state <= send_data;
									end
								hold:
									begin
										if(data_sent)
											begin
											sending_state <= received;
											state <= send_data;
											end
										else
											begin
											sending_state <= hold;
											state <= send_data;
											end
									end
								received:
									begin
										//get signal that data is sent
										if(data_received)
											begin
											//set done signal so next one can start e.g data_complete <= 'b1
											sending_state <= send;
											state <= data_wait;
											end
										else
											begin
											sending_state <= received;
											state <= send_data;
											end
									end
								default: state <= received;
							endcase
						end
					default: state <= data_wait;
				endcase
			end
	end

endmodule

module output_data(

input	logic 			clk,
input logic 			rstn,

input logic [15:0] 	sd_data,

output logic [7:0] 	data_output_low,
output logic [7:0] 	data_output_high

);

typedef enum { output_wait, fill_outputs, send_data} states;
states 					state;

always@(posedge clk or negedge rstn)
	begin
		if(rstn == 'b0)
			begin
			data_output_low 	<= 'd0;
			data_output_high 	<= 'd0;
			state 				<= output_wait;
			end
		else
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
	end

endmodule















