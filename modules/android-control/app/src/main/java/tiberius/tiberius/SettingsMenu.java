package tiberius.tiberius;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

/**
 * SETTINGS ACTIVITY
 */
public class SettingsMenu extends ActionBarActivity {

    // GLOBAL VARIABLES
    // IP ADDRESSES
    private static String webcam_ip   = "192.168.2.105";
    private static String database_ip = "192.168.2.100";
    private static String control_ip  = "192.168.2.101";

    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    /**
     * Start the activity.
     * Update the setting fields with the global values.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings_menu);

        //webcam IP
        EditText edit_webcam = (EditText) findViewById(R.id.webcam_ip);
        edit_webcam.setText(getWebcamIP());
        //database_pi IP
        EditText edit_database = (EditText) findViewById(R.id.database_ip);
        edit_database.setText(getDatabaseIP());
        //control_pi IP
        EditText edit_control = (EditText) findViewById(R.id.control_ip);
        edit_control.setText(getControlIP());

        if (!new Autonomy().missionStopped()) {
            database_thread = new DatabaseThread(this, getDatabaseIP());
            new Thread(database_thread).start();
        }
    }

    /**
     * Return the IP address of the Webcam.
     */
    public String getWebcamIP(){
        return this.webcam_ip;
    }

    /**
     * Set the IP address of the Webcam.
     */
    private void setWebcamIP(String ip){
        this.webcam_ip = ip;
    }

    /**
     * Return the IP address of the Database Pi.
     */
    public String getDatabaseIP(){
        return this.database_ip;
    }

    /**
     * Set the IP address of the Database Pi.
     */
    private void setDatabaseIP(String ip){
        this.database_ip = ip;
    }

    /**
     * Return the IP address of the Control Pi.
     */
    public String getControlIP(){
        return this.control_ip;
    }

    /**
     * Set the IP address of the Control Pi.
     */
    private void setControlIP(String ip){
        this.control_ip = ip;
    }


    /**
     * Called when the user presses the settings button.
     * Updates the global variables of the class and goes to the main menu.
     */
    public void applySettings(View view) {

        //webcam IP
        EditText edit_webcam = (EditText) findViewById(R.id.webcam_ip);
        final String webcam_IP = edit_webcam.getText().toString();

        //database_pi IP
        EditText edit_database = (EditText) findViewById(R.id.database_ip);
        final String database_IP = edit_database.getText().toString();

        //control_pi IP
        EditText edit_control = (EditText) findViewById(R.id.control_ip);
        final String control_IP = edit_control.getText().toString();

        // If there are no changes to the values, go directly to the Main Menu.
        if (webcam_IP.equals(getWebcamIP()) && database_IP.equals(getDatabaseIP())
            && control_IP.equals(getControlIP())){
            this.goMainMenu();
        }

        // Else check if the provided IP addresses are valid.
        else if(validIP(webcam_IP) == false){
            invalidIPAlert(webcam_IP);
        }
        else if(validIP(database_IP) == false){
            invalidIPAlert(database_IP);
        }
        else if(validIP(control_IP) == false){
            invalidIPAlert(control_IP);
        }

        // Else if a mission is running and the user changes the database IP address, stop the mission.
        else if(! new Autonomy().missionStopped() && (! database_IP.equals(getDatabaseIP()))){
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("WARNING!");
            builder.setMessage("In order to change the database IP address, the current mission must stop!\n\n" +
                    "Are you sure you want to change the database IP address and stop the current mission?");
            builder.setCancelable(false);
            builder.setIcon(R.drawable.alert_icon);

            // If "YES" pressed, update the IP addresses and return to the main menu.
            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {

                    // Stop the current mission.
                    database_thread.setIdleMode();
                    new Autonomy().stopMission();
                    database_thread.closeSocket();

                    setWebcamIP(webcam_IP);
                    setDatabaseIP(database_IP);
                    setControlIP(control_IP);

                    goMainMenu();
                }
            });

            // If "NO" pressed, make no changes and remain in the activity.
            builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    // do nothing
                }
            });

            builder.show(); // Display the alert.
        }

        // Else build an Alert to ensure that the user wants to change the IP addresses.
        else {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("WARNING!");
            builder.setMessage("Changes to the IP addresses might affect the operation of the robot. " +
                               "Are you sure you want to proceed?");
            builder.setCancelable(false);
            builder.setIcon(R.drawable.alert_icon);

            // If "YES" pressed, update the IP addresses and return to the main menu.
            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {

                    setWebcamIP(webcam_IP);
                    setDatabaseIP(database_IP);
                    setControlIP(control_IP);

                    goMainMenu();
                }
            });

            // If "NO" pressed, make no changes and remain in the activity.
            builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                   // do nothing
                }
            });

            builder.show(); // Display the alert.
        }
    }

    /**
     * Check if the provided IP address is valid.
     */
    private boolean validIP(String IP){
        String valid_IP = "^(\\d{1,3})\\.(\\d{1,3}).(\\d{1,3}).(\\d{1,3})$";

        // If the IP address doesn't match the valid_IP pattern, return false.
        if(IP.matches(valid_IP) == false){
            return false;
        }
        // Else, the IP address is valid.
        else{
            return true;
        }
    }

    /**
     * Display an invalid IP alert.
     */
    private void invalidIPAlert(String IP){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("ERROR!");
        builder.setMessage("Invalid IP address: " + IP + "! \n\n Please provide an IP address in the form: xxx.xxx.xxx.xxx");
        builder.setCancelable(false);
        builder.setIcon(R.drawable.alert_icon);

        // The user needs to press OK to make the alert disappear.
        builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {}
        });
        builder.show(); // Display the alert.
    }

    /**
     * Go to the Main Menu.
     */
    private void goMainMenu(){
        Intent intent = new Intent(this,MainMenu.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the cancel button.
     * Goes to the main menu without updating the global variables of the class.
     */
    public void cancelSettings(View view) {
        if (!new Autonomy().missionStopped()) {
            database_thread.closeSocket();
        }
        this.goMainMenu();
    }

    /**
     * Called when the user presses the back button.
     * Move to the Main Menu activity.
     */
    @Override
    public void onBackPressed() {
        this.goMainMenu();
    }

    /**
     * Called when the user leaves the activity.
     */
    @Override
    protected void onPause() {
        super.onPause();

        /*
        USER LEAVING THE APPLICATION; IF THE USER LEAVES THE APPLICATION, THE SOCKET WILL NOT HAVE
        BEEN CLOSED SO THE PAUSE MISSION MESSAGE WILL BE SENT TO THE DATABASE.
        A PAUSE MISSION MESSAGE IS SENT WHENEVER THE USER LEAVES THE APPLICATION.
         */
        // If mission is running - pause the current mission.
        if(!new Autonomy().missionStopped()) {
            database_thread.pauseMission();
            database_thread.closeSocket();
        }
    }

    /**
     * Called when the user re-enters the activity (used for re-entering the application).
     */
    @Override
    protected void onRestart() {
        super.onRestart();

        if(!new Autonomy().missionStopped()) {
            new Autonomy().pauseMission();
            // Display an alert that the current mission has been paused.
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("Mission Paused!");
            builder.setMessage("Application was put into the background. The current mission has been paused.");
            builder.setCancelable(false);
            builder.setIcon(R.drawable.alert_icon);
            builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                }
            });
            builder.show();
        }

    }
}
