package tiberius.tiberius;


import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Handler;
import android.os.Looper;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;

/**
 * Thread class to handle the Socket for the Control pi unit.
 *
 * !!!!!!!!!
 * WHEN THE CONTROL UNIT WILL BE ABLE TO READ SPEED DATA DIRECTLY FROM THE DATABASE
 * THIS CLASS SHOULD BE REMOVED.
 *
 * INSTEAD, THE SPEED DATA WILL BE PASSED TO THE DATABASE AND FROM THERE IT WILL BE AVAILABLE
 * TO THE CONTROL UNIT.
 * !!!!!!!!!
 *
 */
public class ControlThread implements Runnable {

    // The PORT of the socket.
    private final static int CONTROL_PORT = 58000;
    // Check for x ms before throwing a TIMETOUT
    private final static int TIMEOUT = 3000;

    // The socket used to send data to the control unit.
    private Socket socket;

    // The context of the activity that called the thread.
    private Context context;

    // The IP address of the control unit.
    private String control_IP;

    // The two motors.
    private Motor left_motor;
    private Motor right_motor;

    // Constructor
    public ControlThread(Context context, String IP, Motor left, Motor right) {
        this.context = context;
        this.control_IP = IP;
        this.left_motor = left;
        this.right_motor = right;
    }

    // Main method
    @Override
    public void run() {

        // Looper that handles any messages that need to be sent to the UI from this thread
        Looper.prepare();

        // try connecting to the Socket
        try {
            socket = new Socket();
            // the socket address on the other end
            SocketAddress socketAddress = new InetSocketAddress(control_IP,CONTROL_PORT);

            socket.connect(socketAddress,TIMEOUT);

            // Send the speed of the motors to the control unit via the socket.
            while (!socket.isClosed()) {
                sendSpeed(left_motor, right_motor);
            }
        }
        catch (UnknownHostException e) {} //not implemented
        // If the socket can't connect to the control unit, display an alert and return to the main menu.
        catch (IOException e) {
            connectionUnavailableAlert();
        }
    }

    /**
     * Send the speeds to the control unit via the socket.
     */
    private void sendSpeed(Motor left_motor, Motor right_motor){
        try {
            // Get the outputstream of the socket.
            PrintWriter output = new PrintWriter(socket.getOutputStream());

            // Output data format : "LEFT_ID,LEFT_SPEED.RIGHT_ID,RIGHT_SPEED."
            String data = left_motor.getID() + "," + Integer.toString(left_motor.getSpeed()) + "." +
                          right_motor.getID() + "," + Integer.toString(right_motor.getSpeed()) + ".";
            // JAVA appends an EOL character (\n) at the end of the String. Python won't recognise this.
            data.replaceAll("\n", "");

            // Send the data via the socket.
            output.print(data);
            output.flush();

            Thread.sleep(30); // sleep for 30 ms before sending the next data.

            // If the connection to the control unit has been dropped, display an alert and return to the main menu.
            if (output.checkError()) {
                connectionLostAlert();
            }
        }
        catch (InterruptedException e) {} //not implemented
        catch (IOException e) {} //not implemented
    }

    /**
     * Display an alert when there can be no connection via the socket.
     */
    private void connectionUnavailableAlert(){
        // Create a handler that displays the alert from the thread on the UI.
        new Handler().post(new Runnable() {
            @Override
            public void run() {
                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                builder.setTitle("Unable to Connect!");
                builder.setMessage("Connection unavailable!\nPlease check the status of the control unit and make sure " +
                                   "that you have set the correct IP address in the Settings.");
                builder.setCancelable(false);
                builder.setIcon(R.drawable.alert_icon);
                builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                   @Override
                   public void onClick(DialogInterface dialog, int which) {
                      new Manual().getWebCamera().stopWebCamera();
                      Intent intent = new Intent(context, MainMenu.class);
                      context.startActivity(intent);
                   }
                });
                builder.show(); // Display the alert.
            }
        });
        // Loop until the button is pressed.
        Looper.loop();
    }

    /**
     * Display an alert when the connection has been lost.
     */
    private void connectionLostAlert(){
        // Close the socket.
        closeSocket();

        // Create a handler that displays the alert from the thread on the UI.
        new Handler().post(new Runnable() {
            @Override
            public void run() {
                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                builder.setTitle("Connection Dropped!");
                builder.setMessage("Whoops! Seems like the connection has been dropped.\n" +
                                   "Please check the status of the control unit.");
                builder.setCancelable(false);
                builder.setIcon(R.drawable.alert_icon);
                builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        new Manual().getWebCamera().stopWebCamera();
                        Intent intent = new Intent(context, MainMenu.class);
                        context.startActivity(intent);
                    }
                });
                builder.show(); // Display the alert.
            }
        });
        // Loop until the button is pressed.
        Looper.loop();
    }

    /**
     * Close the socket connection.
     */
    public void closeSocket(){
        try{
            socket.close();
        }
        catch (IOException e){} //not implemented
    }
}
