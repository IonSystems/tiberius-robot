package tiberius.tiberius;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.app.Service;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

/**
 * AUTONOMY ACTIVITY
 */
public class Autonomy extends ActionBarActivity {

    // GLOBAL VARIABLES & PARAMETERS

    // current status of the mission
    private final static String STOPPED = "STOPPED";
    private final static String RUNNING = "ONGOING";
    private final static String PAUSED  = "PAUSED";

    // mission status - initialised to STOPPED
    private static String mission_status = STOPPED;

    // message for mission parameter fields when no mission is running
    private final static String NOT_AVAILABLE = "N/A";

    // mission state - initialised to N/A (updated from database)
    private static String mission_state = NOT_AVAILABLE;

    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    // Loading spinner
    private ProgressDialog spinner;

    // Timer object to control the updating of the mission fields.
    private Timer timer;

    // The IP webcamera object.
    private static WebCamera webCamera;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_autonomy);

        // Create the webcam object => communicating to the web camera.
        WebView webView = (WebView) findViewById(R.id.webcam_autonomy);
        webCamera = new WebCamera(this,webView);
        webCamera.startWebCamera();

        // Create the socket thread for the autonomy mode.
        final String database_IP = new SettingsMenu().getDatabaseIP();
        database_thread = new DatabaseThread(Autonomy.this,database_IP);
        new Thread(database_thread).start();

        // Update the mission fields and buttons every 200ms.
        updateMissionFields();

        // If the mission is stopped, display a spinner before connecting to the database unit.
        if (missionStopped()) {
            // Display a loading spinner for 2.8 seconds < TIMEOUT time for the connection.
            spinner = ProgressDialog.show(this, "Please wait...", "Connecting to the database unit...", true, false);

            new Thread(new Runnable() {
                @Override
                public void run() {
                    Looper.prepare();
                    try {
                        Thread.sleep(2800);
                        spinner.dismiss();

                        // If the application was closed without stopping a mission then Tiberius will be in AUTONOMY_PAUSE mode.
                        // Retrieve and display the paused mission.
                        if(database_thread.missionPaused()){
                            // Set latitude, longitude and object
                            final String gps_parameters = database_thread.getMissionGPS();
                            String gps_parts [] = gps_parameters.split(",");
                            new MissionSelection().setLatitude(gps_parts[0]); // latitude
                            new MissionSelection().setLongitude(gps_parts[1]); // longitude
                            new MissionSelection().setObject(database_thread.getMissionObject());
                            new Autonomy().pauseMission();

                            // Display an alert.
                            AlertDialog.Builder builder = new AlertDialog.Builder(Autonomy.this);
                            builder.setTitle("MISSION RETRIEVED!");
                            builder.setMessage("Retrieved latest paused mission from the database.");
                            builder.setCancelable(false);
                            builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {}
                            });
                            builder.show();
                        }

                    } catch (InterruptedException e) {}
                    Looper.loop();
                }
            }).start();
        }
    }

    /**
     * Start a new mission
     */
    public void startMission() {
        setMissionStatus(RUNNING);
    }

    /**
     * Pause the current mission
     */
    public void pauseMission() {
        setMissionStatus(PAUSED);
    }

    /**
     * Resume the mission
     */
    private void resumeMission() {
        setMissionStatus(RUNNING);
    }

    /**
     * Stop the current mission
     */
    public void stopMission() {
        setMissionStatus(STOPPED);
    }

    /**
     * Go to the Mission Selection activity
     * */
    private void selectMission() {
        webCamera.stopWebCamera();
        timer.cancel();
        database_thread.closeSocket();
        Intent intent = new Intent(this, MissionSelection.class);
        startActivity(intent);
    }

    /**
     * Set the current status of the mission.
     */
    private void setMissionStatus(String mission_status) {
        this.mission_status = mission_status;
    }

    /**
     * Get the current status of the mission.
     */
    private String getMissionStatus() {
        return this.mission_status;
    }

    /**
     * Set the current state of the mission.
     */
    public void setMissionState(String mission_state) {
        // Many states have the form "MISSION_STATE"; need to replace _ with (new line).
        mission_state = mission_state.replaceAll("_","\n");
        this.mission_state = mission_state;
    }

    /**
     * Get the latest state of the mission.
     */
    private String getMissionState() {
        return this.mission_state;
    }


    /**
     * Update the Mission Command Buttons and Parameter Fields every 200ms.
     */
    private void updateMissionFields(){

        timer = new Timer();

        TimerTask timerTask = new TimerTask() {

            // Buttons
            Button button_start  = (Button)   findViewById(R.id.start_mission_btn);
            Button button_stop   = (Button)   findViewById(R.id.stop_mission_btn);

            // Textviews
            TextView text_latitude  = (TextView) findViewById(R.id.autonomy_mission_latitude);
            TextView text_longitude = (TextView) findViewById(R.id.autonomy_mission_longitude);
            TextView text_object    = (TextView) findViewById(R.id.autonomy_mission_object);
            TextView text_mission   = (TextView) findViewById(R.id.autonomy_mission);
            TextView text_status    = (TextView) findViewById(R.id.autonomy_status);

            @Override
            public void run() {
                Autonomy.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // IF MISSION IS STOPPED:
                        if (missionStopped()){
                            button_start.setText(R.string.mission_start_btn);
                            button_stop.setEnabled(false); // disable STOP button

                            text_latitude.setText(NOT_AVAILABLE);
                            text_longitude.setText(NOT_AVAILABLE);
                            text_object.setText(NOT_AVAILABLE);
                            text_object.setBackgroundColor(Color.WHITE);
                            // Update STATUS field
                            text_status.setText(NOT_AVAILABLE);
                        }

                        else {
                            // IF MISSION IS PAUSED:
                            if (missionPaused()){
                                button_start.setText(R.string.mission_resume_btn);
                                button_stop.setEnabled(true); // enable STOP button
                            }
                            // IF MISSION IS RUNNING:
                            else {
                                button_start.setText(R.string.mission_pause_btn);
                                button_stop.setEnabled(true); // enable STOP button
                            }

                            text_latitude.setText(new MissionSelection().getLatitude());
                            text_longitude.setText(new MissionSelection().getLongitude());
                            text_object.setText("");
                            text_object.setBackground(getResources().getDrawable(new MissionSelection().getObjectIconID()));
                            // Update STATUS field
                            text_status.setText(getMissionState());
                        }

                        // Update MISSION field
                        text_mission.setText(getMissionStatus());
                    }
                });
            }
        };

        // Schedule the fields to be updated every 200ms.
        timer.schedule(timerTask, 0, 200);
    }

    /**
     * Check if the mission has been stopped.
     * If stopped return true.
     */
    public boolean missionStopped() {
        if (getMissionStatus().equals(STOPPED)) { return true; }
        else                                    { return false;}
    }

    /**
     * Check if the mission has been paused.
     * If paused return true.
     */
    private boolean missionPaused() {
        if (getMissionStatus().equals(PAUSED)) { return true; }
        else                                   { return false;}
    }

    /**
     * The start button has been pressed.
     */
    public void startPressed(View view) {
        // check the current text of the button.
        Button start_btn = (Button) findViewById(R.id.start_mission_btn);
        String operation = start_btn.getText().toString();
        // possible mission statuses
        String start  = getResources().getString(R.string.mission_start_btn);
        String pause  = getResources().getString(R.string.mission_pause_btn);
        String resume = getResources().getString(R.string.mission_resume_btn);
        // START MISSION - SELECT MISSION
        if (operation.equals(start)) {
            this.selectMission();
        }
        // PAUSE MISSION
        else if (operation.equals(pause)) {
            database_thread.pauseMission();
            pauseMission();
        }
        // RESUME MISSION
        else if (operation.equals(resume)){
            database_thread.resumeMission();
            resumeMission();
        }
    }

    /**
     * The stop button has been pressed.
     */
    public void stopPressed(View view) {
        // Display an alert before stopping the mission.
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Warning!");
        builder.setMessage("Are you sure you want to stop the current mission?");
        builder.setCancelable(false);
        builder.setIcon(R.drawable.alert_icon);

        // If "YES" pressed, stop the current mission.
        builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                database_thread.setIdleMode();
                stopMission();
            }
        });

        // If "NO" pressed, make no changes.
        builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {}});

        builder.show(); // Display the alert.
    }

    /**
     * Return the WebCamera object of the class.
     */
    public WebCamera getWebCamera(){
        return webCamera;
    }


    /**
     * Go to the Main Menu
     */
    private void goMainMenu(){
        Intent intent = new Intent(this,MainMenu.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the menu button.
     * Move to the Main Menu activity.
     */
    public void goMenu(View view) {
        webCamera.stopWebCamera();
        timer.cancel();
        timer.purge();
        database_thread.closeSocket();
        this.goMainMenu();
    }

    /**
     * Called when the user presses the back button
     * Move to the Main Menu activity.
     */
    @Override
    public void onBackPressed() {
        webCamera.stopWebCamera();
        timer.cancel();
        timer.purge();
        database_thread.closeSocket();
        this.goMainMenu();
    }

    /**
     * Called when the activity is stopped.
     */
    @Override
    protected void onStop() {
        super.onStop();
        // Ensure that the loading spinner is dismissed.
        spinner = new ProgressDialog(this);
        spinner.dismiss();
    }

    /**
     * Called when the user leaves the activity.
     */
    @Override
    protected void onPause() {
        super.onPause();
        webCamera.stopWebCamera();
        timer.cancel();
        timer.purge();
        /*
        USER LEAVING THE APPLICATION; IF THE USER LEAVES THE APPLICATION, THE SOCKET WILL NOT HAVE
        BEEN CLOSED SO THE PAUSE MISSION MESSAGE WILL BE SENT TO THE DATABASE.
        A PAUSE MISSION MESSAGE IS SENT WHENEVER THE USER LEAVES THE APPLICATION.
         */
        // If mission is running - pause the current mission.
        if(!missionStopped()) {
            database_thread.pauseMission();
        }
        database_thread.closeSocket();
    }

    /**
     * Called when the user re-enters the activity (used for re-entering the application).
     */
    @Override
    protected void onRestart() {
        super.onRestart();

        // Create the webcam object => communicating to the web camera.
        WebView webView = (WebView) findViewById(R.id.webcam_autonomy);
        webCamera = new WebCamera(this,webView);
        webCamera.startWebCamera();

        // Create the socket thread for the autonomy mode.
        final String database_IP = new SettingsMenu().getDatabaseIP();
        database_thread = new DatabaseThread(Autonomy.this,database_IP);
        new Thread(database_thread).start();

        // Update the mission fields and buttons every 200ms.
        updateMissionFields();

        if(!missionStopped()) {
            pauseMission();
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
