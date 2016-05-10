//
// Tiberius CAN bus tester
// -----------------------
//
// Simple C# program to allow user to send UDP packets to the Tiberius
// an ethernet-CAN bridge unit that in turn connects to four CAN nodes, 
// one for each driven wheel.
//
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Net;
using System.Net.Sockets;



namespace Tiberius_UDP_test {
    public partial class Form1 : Form {

        //---------------------------------------------------------------------
        // Definition of constants
        //
        const string MBED_IP = "192.168.0.200";
        const string MBED_LISTEN_PORT = "43442";
        const int PACKET_SIZE = 32;

        const int MAX_STEPS = 20000;
        const int MAX_CAN_BYTES = 8;

        enum SYS_commands {
            PID_P_GAIN = 0,
            TOGGLE_LED1,
            MOTOR_SPEED,
            MOTOR_PWM,
            STEERING_MOVE_REL,
            STEERING_MOVE_ABS,
            STEERING_ANGLE,
        };
        enum MBED_target {
            FRONT_LEFT = 0,
            FRONT_RIGHT,
            REAR_LEFT,
            REAR_RIGHT,
            Bridge,
        };
        enum cmd_dest_t {
            LOCAL = 0x00,
            CANBUS = 0x40,
        };
        enum type_move_t {
            ABSOLUTE = 0,
            RELATIVE = 1,
        };
        enum motor_direction_t {
            CLOCKWISE     = 0,
            ANTICLOCKWISE = 1,
        };

        //---------------------------------------------------------------------
        // Ethernet related declarations
        //
        int MBED_listen_port;
        IPAddress send_to_address;
        string mbed_ip;
        UdpClient client = new UdpClient();

        //---------------------------------------------------------------------
        // Global variables
        //
        byte[] packet_data = new byte[PACKET_SIZE];
        byte[] array = new byte[4];

        //---------------------------------------------------------------------
        // Main form
        //
        public Form1() {
            InitializeComponent();
        }
        //---------------------------------------------------------------------
        // Init actions when form is started
        //
        private void Form1_Load(object sender, EventArgs e) {
            groupBox1.Enabled = false;
            groupBox4.Enabled = false;
            groupBox5.Enabled = false;
            textBox2.Text = MBED_IP;
            textBox11.Text = MBED_LISTEN_PORT;
        }
        //---------------------------------------------------------------------
        // Initialise UDP output channel 'IP' and 'port'
        //
        private void button3_Click(object sender, EventArgs e) {
            MBED_listen_port = int.Parse(textBox11.Text);
            if (MBED_listen_port < 40000) {
                textBox1.AppendText("Port number " + textBox11.Text + " is too low." + Environment.NewLine);
                return;
            }
            textBox1.AppendText("Port = " + textBox11.Text + Environment.NewLine);
            mbed_ip = textBox2.Text;
            send_to_address = IPAddress.Parse(textBox2.Text);
            textBox1.AppendText("IP address = " + textBox2.Text + Environment.NewLine);
            groupBox1.Enabled = true;
            groupBox4.Enabled = true;
            groupBox5.Enabled = true;
        }
        //---------------------------------------------------------------------
        // 'exit' button from dropdown menu
        //
        private void exitToolStripMenuItem_Click(object sender, EventArgs e) {
            Close();
        }
        //---------------------------------------------------------------------
        // Send UDP packet to toggle LED1 on any of the MBEDs on the CAN network
        //
        private void button1_Click(object sender, EventArgs e) {

            int packet_length = 0, packet_pt = 0, packet_ID = 0, CAN_bytes;

            client.Connect(mbed_ip, MBED_listen_port);

            clear_packet();
            packet_pt = 0; CAN_bytes = 0;
            switch ((MBED_target)comboBox1.SelectedIndex) {
                case MBED_target.Bridge:
                    packet_data[packet_pt++] = (byte)cmd_dest_t.LOCAL;
                    packet_data[packet_pt++] = (byte)SYS_commands.TOGGLE_LED1;
                    packet_length = packet_pt;
                    textBox1.AppendText("Local LED toggle command" + Environment.NewLine);
                    break;
                case MBED_target.FRONT_LEFT:
                case MBED_target.FRONT_RIGHT:
                case MBED_target.REAR_LEFT:
                case MBED_target.REAR_RIGHT:
                    packet_data[packet_pt++] = (byte)cmd_dest_t.CANBUS;
                    packet_ID = 0x100 + comboBox1.SelectedIndex;
                    array = BitConverter.GetBytes(packet_ID);
                    Array.Copy(array, 0, packet_data, packet_pt, 4);
                    packet_pt += 4;
                    packet_data[packet_pt++] = (byte)SYS_commands.TOGGLE_LED1;
                    packet_pt += 7;   // skip othet 7 byes of CAN packet
                    CAN_bytes += 1;
                    array = BitConverter.GetBytes(CAN_bytes);
                    Array.Copy(array, 0, packet_data, packet_pt, 4);
                    packet_pt += 4;
                    packet_length = packet_pt;
                    textBox1.AppendText("CANbus LED toggle command" + Environment.NewLine);
                    break;
                default:
                    textBox1.AppendText("BAD toggle command" + Environment.NewLine);
                    break;

            }
            client.Send(packet_data, packet_length);
            textBox1.AppendText("LED toggle command sent" + Environment.NewLine);
        }
        //---------------------------------------------------------------------
        // 
        //
        private void button2_Click(object sender, EventArgs e) {
        }
        
        //---------------------------------------------------------------------
        // Send UDP packet to stepper motor
        //
        private void button5_Click(object sender, EventArgs e) {

            int packet_length = 0, packet_pt = 0, packet_ID = 0, nos_steps = 0, CAN_bytes;

            client.Connect(mbed_ip, MBED_listen_port);

            clear_packet();
            packet_pt = 0;
            CAN_bytes = 0;

            packet_data[packet_pt++] = (byte)cmd_dest_t.CANBUS;
            packet_ID = 0x100 + comboBox3.SelectedIndex;
            array = BitConverter.GetBytes(packet_ID);
            Array.Copy(array, 0, packet_data, packet_pt, 4);
            packet_pt += 4;
            if (comboBox4.SelectedIndex == (int)type_move_t.RELATIVE) {
                packet_data[packet_pt++] = (byte)SYS_commands.STEERING_MOVE_REL;
            } else {
                packet_data[packet_pt++] = (byte)SYS_commands.STEERING_MOVE_ABS;
            }
                
            CAN_bytes += 1;
            if (Int32.TryParse(textBox13.Text, out nos_steps)) {
                textBox1.AppendText("Steps requested = " + nos_steps + Environment.NewLine);
            }
            else {
                textBox1.AppendText("String could not in integer format." + Environment.NewLine);
                return;
            }
            if (Math.Abs(nos_steps) > MAX_STEPS) {
                textBox1.AppendText("Step count > MAX(" + MAX_STEPS + ")" + Environment.NewLine);
                return;
            }
            array = BitConverter.GetBytes(nos_steps);
            Array.Copy(array, 0, packet_data, packet_pt, 4);
            CAN_bytes += 4;
            packet_pt += 4;
            packet_pt += (MAX_CAN_BYTES - CAN_bytes);
            array = BitConverter.GetBytes(CAN_bytes);
            Array.Copy(array, 0, packet_data, packet_pt, 4);
            packet_pt += 4;
            packet_length = packet_pt;
            textBox1.AppendText("CANbus stepper motor command" + Environment.NewLine);
            client.Send(packet_data, packet_length);
        }
        //---------------------------------------------------------------------
        // Send UDP packet to DC motor with PWM value (0->100%)
        //
        private void button4_Click(object sender, EventArgs e) {
            int packet_length = 0, packet_pt = 0, packet_ID = 0, CAN_bytes, direction, PWM_value;

            client.Connect(mbed_ip, MBED_listen_port);

            clear_packet();
            packet_pt = 0;
            CAN_bytes = 0;

            packet_data[packet_pt++] = (byte)cmd_dest_t.CANBUS;
            packet_ID = 0x100 + comboBox3.SelectedIndex;
            array = BitConverter.GetBytes(packet_ID);
            Array.Copy(array, 0, packet_data, packet_pt, 4);
            packet_pt += 4;
            packet_data[packet_pt++] = (byte)SYS_commands.MOTOR_PWM;
            CAN_bytes += 1;
            direction = (int)motor_direction_t.CLOCKWISE;
            if (numericUpDown1.Value < 0) {
                direction = (int)motor_direction_t.ANTICLOCKWISE;
            }
            PWM_value = (int)Math.Abs(numericUpDown1.Value);
            textBox1.AppendText("Direction = " + direction + Environment.NewLine);
            textBox1.AppendText("PWM duty cycle (%) = " + PWM_value + Environment.NewLine);
            packet_data[packet_pt++] = (byte)direction;
            CAN_bytes += 1;
            packet_data[packet_pt++] = (byte)PWM_value;
            CAN_bytes += 1;
            packet_pt += (MAX_CAN_BYTES - CAN_bytes);
            array = BitConverter.GetBytes(CAN_bytes);
            Array.Copy(array, 0, packet_data, packet_pt, 4);
            packet_pt += 4;
            packet_length = packet_pt;
            textBox1.AppendText("CANbus DC motor command" + Environment.NewLine);
            client.Send(packet_data, packet_length);
        }
        //---------------------------------------------------------------------
        // Local functions
        //---------------------------------------------------------------------
        // Set packet_data buffer to all zero
        //
        void clear_packet() {
            Array.Clear(packet_data, 0, packet_data.Length);
        }
    }
}
