package tiberius.tiberius;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;

/**
 * MAIN MENU ACTIVITY
 */
public class MainMenu extends ActionBarActivity {

    /* GLOBAL PARAMETERS */
    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);

        if (!new Autonomy().missionStopped()) {
            database_thread = new DatabaseThread(this, new SettingsMenu().getDatabaseIP());
            new Thread(database_thread).start();
        }
    }

    /**
     * Called when the user presses the autonomy button
     * Move to the Autonomy activity.
     */
    public void goAutonomy(View view){
        if (!new Autonomy().missionStopped()) {
            database_thread.closeSocket();
        }
        Intent intent = new Intent(this, Autonomy.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the manual button
     * Move to the Manual activity.
     */
    public void goManual(View view){
        // if a mission is currently running ask the user if it needs to be stopped.
        // Manual mode can't run in parallel with a mission.
        if (!new Autonomy().missionStopped()) {

            // Display an alert before stopping the mission.
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("Warning!");
            builder.setMessage("The current mission needs to stop before entering the Manual mode.\n" +
                               "Would you like to stop the current mission?");
            builder.setCancelable(false);
            builder.setIcon(R.drawable.alert_icon);

            // If "YES" pressed, stop the current mission.
            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    // Send IDLE to the database and move to the Manual activity.
                    database_thread.setIdleMode();
                    database_thread.closeSocket();
                    new Autonomy().stopMission();
                    Intent intent = new Intent(MainMenu.this, Manual.class);
                    startActivity(intent);
                }
            });

            // If "NO" pressed, make no changes.
            builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                }
            });

            builder.show(); // Display the alert.
        }
        // else enter the Manual activity.
        else {
            if (!new Autonomy().missionStopped()) {
                database_thread.closeSocket();
            }
            Intent intent = new Intent(this, Manual.class);
            startActivity(intent);
        }
    }

    /**
     * Called when the user presses the database button
     * Move to the Database activity.
     */
    public void goDatabase(View view){
        if (!new Autonomy().missionStopped()) {
            database_thread.closeSocket();
        }
        Intent intent = new Intent(this, Database.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the settings button
     * Move to the Settings activity.
     */
    public void goSettings(View view){
        if (!new Autonomy().missionStopped()) {
            database_thread.closeSocket();
        }
        Intent intent = new Intent(this, SettingsMenu.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the return button
     */
    @Override
    public void onBackPressed() {}// not implemented

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
