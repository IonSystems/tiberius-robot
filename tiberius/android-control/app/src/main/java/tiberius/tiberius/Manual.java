package tiberius.tiberius;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Looper;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.widget.SeekBar;
import android.widget.TextView;

/**
 * MANUAL ACTIVITY
 */
public class Manual extends ActionBarActivity {
    /** GLOBAL VARIABLES & PARAMETERS */

    // The center position of the progress bar {0...255...510}.
    private final static int CENTER_PROGRESS = 255;

    // The thread handling the socket sending speed data to the control unit.
    private ControlThread control_thread;

    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    // Loading spinner
    private ProgressDialog spinner;

    // The IP webcamera object.
    private static WebCamera webCamera;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manual);

        // Create the webcam object => communicating to the web camera.
        WebView webView = (WebView) findViewById(R.id.webcam_manual);
        webCamera = new WebCamera(this,webView);
        webCamera.startWebCamera();

        // Get the left and right speed fields.
        final TextView edit_left  = (TextView) findViewById(R.id.left_speed);
        final TextView edit_right = (TextView) findViewById(R.id.right_speed);

        // Create the left and right motor items.
        final Motor left_motor  = new Motor("Left");
        final Motor right_motor = new Motor("Right");

        // Get the left and right seekbar items.
        final SeekBar sbar_left = (SeekBar) findViewById(R.id.left_seekbar);
        final SeekBar sbar_right = (SeekBar) findViewById(R.id.right_seekbar);

        // Initial update of the speed text fields.
        updateSpeedText(edit_left,left_motor.getSpeed());
        updateSpeedText(edit_right, right_motor.getSpeed());

        // Create the socket thread for the autonomy mode.
        String database_IP = new SettingsMenu().getDatabaseIP();
        database_thread = new DatabaseThread(Manual.this,database_IP);
        new Thread(database_thread).start();

        // Display a loading spinner for 2.8 seconds < TIMEOUT time for the connection.
        spinner = ProgressDialog.show(this, "Please wait...", "Connecting to the control unit...", true, false);

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(2800);
                    // Inform the database that the Manual Mode has started.
                    database_thread.setManualMode();
                    spinner.dismiss();

                    // Wait for the control unit to open its socket.
                    Thread.sleep(1000);
                    Looper.prepare();
                    // Create the control thread => sending speed data to the control unit.
                    String control_IP = new SettingsMenu().getControlIP();
                    control_thread = new ControlThread(Manual.this,control_IP,left_motor,right_motor);
                    new Thread(control_thread).start();

                } catch (InterruptedException e) {
                }

            }
        }).start();

        // Get the progress of the seekbars and update the motors' speed.
        // Creates a Listener for changes to the progress.
        getSeekbarProgress(sbar_left, edit_left, left_motor);
        getSeekbarProgress(sbar_right, edit_right, right_motor);
    }

    /**
     * Get the progress of the seekbar.
     */
    private void getSeekbarProgress(final SeekBar seekBar, final TextView textView, final Motor motor) {
        // Get the data from the seekbar
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @Override // Whenever the progress bar is changed.
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                int speed = seekBar.getProgress();
                motor.setSpeed(speed);
                updateSpeedText(textView, motor.getSpeed());
            }

            @Override // NOT IMPLEMENTED
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            // Whenever the user stops touching the progress bar.
            @Override  // Reset the progress bar and the speed to the central positions.
            public void onStopTrackingTouch(SeekBar seekBar) {
                seekBar.setProgress(CENTER_PROGRESS);
                motor.stopMotor();
                updateSpeedText(textView, motor.getSpeed());
            }
        });
    }

    /**
     * Update the text field with the speed value.
     */
    private void updateSpeedText(TextView textView, int speed) {
        textView.setText(Integer.toString(speed));
    }

    /**
     * Return the WebCamera object of the class.
     */
    public WebCamera getWebCamera(){
        return webCamera;
    }

    /**
     * Go to the Main Menu.
     */
    private void goMainMenu(){
        Intent intent = new Intent(this, MainMenu.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the menu button
     * Move to the Main Menu activity.
     */
    public void goMenu(View view) {
        webCamera.stopWebCamera();
        database_thread.setIdleMode(); // leaving manual mode
        database_thread.closeSocket();
        control_thread.closeSocket();
        this.goMainMenu();
    }

    /**
     * Called when the user presses the back button
     * Move to the Main Menu activity.
     */
    @Override
    public void onBackPressed() {
        webCamera.stopWebCamera();
        database_thread.setIdleMode();
        database_thread.closeSocket();
        control_thread.closeSocket();
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
        webCamera.stopWebCamera();
        database_thread.setIdleMode();
        database_thread.closeSocket();
        control_thread.closeSocket();
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