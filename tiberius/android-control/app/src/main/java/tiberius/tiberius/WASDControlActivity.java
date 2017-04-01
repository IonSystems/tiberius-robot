package tiberius.tiberius;

import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.SeekBar;
import android.widget.TextView;

/**
 * MANUAL ACTIVITY
 */
public class WASDControlActivity extends ActionBarActivity {
    /** GLOBAL VARIABLES & PARAMETERS */

    // The center position of the progress bar {0...255...510}.
    private final static int CENTER_PROGRESS = 100;

    // The thread handling the socket sending speed data to the control unit.
    private ControlThread control_thread;

    // Loading spinner
    private ProgressDialog spinner;

    TextView left_text, right_text;

    Motor left_motor, right_motor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manual);

        // Get the left and right seekbar items.



        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(getBaseContext());
        String control_IP = SP.getString("api_ip_address", "192.168.0.24");
        control_thread = new ControlThread(WASDControlActivity.this,control_IP);
        new Thread(control_thread).start();


    }



    private void goMainMenu(){
        Intent intent = new Intent(this, MainMenuActivity.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the menu button
     * Move to the Main Menu activity.
     */
    public void goMenu(View view) {
        this.goMainMenu();
    }

    /**
     * Called when the user presses the back button
     * Move to the Main Menu activity.
     */
    @Override
    public void onBackPressed() {
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
     * Called when the user leaves the app.
     */
    @Override
    protected void onPause() {
        super.onPause();
    }

    /**
     * Called when the user re-enters the application.
     */
    @Override
    protected void onRestart() {
        super.onRestart();
        this.goMainMenu();
    }

}