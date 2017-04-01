package tiberius.tiberius;


import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Handler;
import android.os.Looper;
import android.widget.TextView;

public class ControlThread implements Runnable {

    private ControlMode control_mode;

    // The context of the activity that called the thread.
    private Context context;

    // The IP address of the control unit.
    private String control_IP;

    // The two motors.
    private Motor left_motor, right_motor;

    private TextView left_text, right_text;
    private HTTPInterface http;


    // Constructor
    public ControlThread(Context context, String IP, Motor left, Motor right, TextView tv_left, TextView tv_right) {
        this.context = context;
        this.control_IP = IP;
        this.left_motor = left;
        this.right_motor = right;

        this.left_text = tv_left;
        this.right_text = tv_right;

        this.http = new HTTPInterface(context, IP);

        this.control_mode = ControlMode.THUMB;
    }

    public ControlThread(Context context, String IP){
        this.context = context;
        this.control_IP = IP;

        this.control_mode = ControlMode.WASD;

    }

    private void goForward(){

    }

    private void goBackwards(){

    }

    private void goLeft(){

    }

    private void goRight(){

    }

    // Main method
    @Override
    public void run() {
            while (true) {
//                boolean success = true;
//                Thread t = new Thread(new Runnable() {
//                    public void run()
//                    {
                        boolean result = sendSpeed(left_motor, right_motor);
                        if (!result) {
//                            success = false;
//                            t.setName("FAIL");
                        }
//                    }
//                });
//                t.start();

//                if(!success){
//                    connectionLostAlert();
//                }

                //Delay between each request to reduce stress on API.
                try {
                    Thread.sleep(200);
                }catch(InterruptedException e){
                    e.printStackTrace();
                }
            }
    }

    private boolean sendSpeed(Motor left_motor, Motor right_motor){
        http.sendSpeeds(left_motor.getSpeed(), right_motor.getSpeed());
        setSpeedText(left_motor.getSpeed(), right_motor.getSpeed());
        return true;
    }

    /**
     * Display an alert when the connection has been lost.
     */
    private void connectionLostAlert(){

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
                        Intent intent = new Intent(context, MainMenuActivity.class);
                        context.startActivity(intent);
                    }
                });
                builder.show(); // Display the alert.
            }
        });
        // Loop until the button is pressed.
        Looper.loop();
    }

    private void setSpeedText(int left_speed, int right_speed){
        final TextView lt = this.left_text;
        final TextView rt = this.right_text;
        final int ls = left_speed;
        final int rs = right_speed;

        //We can't change views from this thread, se we do it in UI thread.
        this.left_text.post(new Runnable() {
            public void run() {
                lt.setText(Integer.toString(ls));
            }
        });

        this.right_text.post(new Runnable() {
            public void run() {
                rt.setText(Integer.toString(rs));
            }
        });

    }

}
