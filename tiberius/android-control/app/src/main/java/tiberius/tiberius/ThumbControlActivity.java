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
public class ThumbControlActivity extends ActionBarActivity {
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
        final SeekBar sbar_left = (SeekBar) findViewById(R.id.left_seekbar);
        final SeekBar sbar_right = (SeekBar) findViewById(R.id.right_seekbar);
        int max_seekbar_left = sbar_left.getMax();
        int max_seekbar_right = sbar_right.getMax();

        // Create the left and right motor items.
        this.left_motor  = new Motor("Left", 0, max_seekbar_left);
        this.right_motor = new Motor("Right",0, max_seekbar_right);

        this.left_text = (TextView) findViewById(R.id.left_speed_text);
        this.right_text = (TextView) findViewById(R.id.right_speed_text);

        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(getBaseContext());
        String control_IP = SP.getString("api_ip_address", "192.168.0.24");
        control_thread = new ControlThread(ThumbControlActivity.this,control_IP,left_motor,right_motor, left_text, right_text);
        new Thread(control_thread).start();

        getSeekbarProgress(sbar_left, left_motor);
        getSeekbarProgress(sbar_right, right_motor);
    }

    private void getSeekbarProgress(final SeekBar seekBar, final Motor motor) {
        // Get the data from the seekbar
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @Override // Whenever the progress bar is changed.
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                int speed = seekBar.getProgress();
                motor.setSpeed(speed);
            }

            @Override // NOT IMPLEMENTED
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            // Whenever the user stops touching the progress bar.
            @Override  // Reset the progress bar and the speed to the central positions.
            public void onStopTrackingTouch(SeekBar seekBar) {
                seekBar.setProgress(CENTER_PROGRESS);
                motor.stopMotor();
            }
        });
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