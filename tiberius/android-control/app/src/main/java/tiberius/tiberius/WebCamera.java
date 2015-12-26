package tiberius.tiberius;

import android.app.Activity;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebView;
import java.util.Timer;
import java.util.TimerTask;

/**
 * !!!!!!!!!!!!!!!!!!!!!!
 * IMPORTANT
 *
 * THE FUNCTIONALITY OF THIS CLASS HASN'T BEEN TESTED.
 *
 * !!!!!!!!!!!!!!!!!!!!!!
 *
 * Class to handle the communication to the Web Camera.
 */
public class WebCamera{
    // GLOBAL VARIABLES & PARAMETERS

    // The context of the activity that instantiated the class.
    private Activity activity;
    // The webcam object.
    private WebView webcam;
    // Timer object to control the refreshing of the snapshot.
    private Timer timer;

    String webcam_IP = new SettingsMenu().getWebcamIP();
    String user  = "admin";
    String pwd   = "";
    // Commands sent to the web camera.
    final String SNAPSHOT   = "http://" + webcam_IP + "/snapshot.cgi?user=" + user + "&pwd=" + pwd + "&resolution=32";
    final String CENTER     = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=25";
    final String UP         = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=0";
    final String STOP_UP    = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=1";
    final String DOWN       = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=2";
    final String STOP_DOWN  = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=3";
    final String LEFT       = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=4";
    final String STOP_LEFT  = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=5";
    final String RIGHT      = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=6";
    final String STOP_RIGHT = "http://" + webcam_IP + "/decoder_control.cgi?user=" + user + "&pwd=" + pwd + "&command=7";

    /**
     * Constructor
     */
    public WebCamera(Activity activity, WebView webcam) {
        this.activity = activity;
        this.webcam = webcam;

        timer = new Timer();
    }

    /**
     * Start the main operation of the webcamera.
     */
    public void startWebCamera(){
        initialiseWebCamera();
        refreshWebCamera();
        moveWebCamera();
    }

    /**
     * Initialise the webcamera - capture initial snapshot.
     */
    private void initialiseWebCamera(){

        // TODO Initiliase webcam parameters.

        // Capture initial snapshot.
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                webcam.loadUrl(SNAPSHOT);
            }
        });
    }

    /**
     * Refresh the snapshot every 250 ms.
     */
    private void refreshWebCamera(){
        // Refresh the snapshot.
        TimerTask timerTask = new TimerTask() {
            @Override
            public void run() {
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        webcam.loadUrl(SNAPSHOT);
                    }
                });
            }
        };

        // Schedule the snapshot to be refreshed every 250 ms.
        timer.schedule(timerTask, 0, 250);
    }

    /**
     * Move the camera based on the user's gestures.
     */
    private void moveWebCamera(){
        webcam.setOnTouchListener(new View.OnTouchListener() {
            float start_x = 0;
            float start_y = 0;

            float x_past = 0;
            float y_past = 0;

            String dir  = "";
            String dir_past = "";

            @Override
            public boolean onTouch(View v, MotionEvent event) {

                // STARTING EVENT - FIRST TOUCH
                if(event.getAction() == MotionEvent.ACTION_DOWN){
                    start_x = event.getX();
                    start_y = event.getY();

                    return true;
                }

                // MOVING EVENT - MOVE FINGER
                else if(event.getAction() == MotionEvent.ACTION_MOVE){
                    float x = event.getX();
                    float y = event.getY();

                    // GET CURRENT DIRECTION
                    if (x > (start_x + 50)){
                        dir = "RIGHT";
                    }
                    else if (x < (start_x - 50)) {
                        dir = "LEFT";
                    }
                    else if (y < (start_y - 50)){
                        dir = "UP";
                    }
                    else if (y > (start_y + 50)){
                        dir = "DOWN";
                    }
                    else{
                        dir = "STOP";
                    }

                    // FIND WHETHER THE DIRECTION HAS CHANGED
                    if (!dir.equals(dir_past)){
                        if (dir.equals("RIGHT")){
                            webcam.loadUrl(RIGHT);
                        }
                        else if (dir.equals("LEFT")){
                            webcam.loadUrl(LEFT);
                        }
                        else if (dir.equals("UP")){
                            webcam.loadUrl(UP);
                        }
                        else if (dir.equals("DOWN")){
                            webcam.loadUrl(DOWN);
                        }
                    }

                    // KEEP TRACK OF THE PREVIOUS MOVES
                    x_past = x;
                    y_past = y;
                    dir_past = dir;


                    // The starting points change if the direction is abruptly changed.
                    if ((x < x_past) && (dir.equals("RIGHT"))){
                        start_x = x_past;
                        start_y = y_past;
                        webcam.loadUrl(STOP_RIGHT);
                    }
                    else if ((x > x_past) && (dir.equals("LEFT"))){
                        start_x = x_past;
                        start_y = y_past;
                        webcam.loadUrl(STOP_LEFT);
                    }

                    if ((y > y_past) && (dir.equals("UP"))){
                        start_x = x_past;
                        start_y = y_past;
                        webcam.loadUrl(STOP_UP);
                    }

                    else if ((y < y_past) && (dir.equals("DOWN"))){
                        start_x = x_past;
                        start_y = y_past;
                        webcam.loadUrl(STOP_DOWN);
                    }

                    return true;
                }

                // ENDING EVENT - RAISE FINGER
                else if(event.getAction() == MotionEvent.ACTION_UP){
                    // TODO Center the Webcam before leaving - Center on double click
                    webcam.loadUrl(CENTER);
                    return true;
                }

                return false;

            }
        });
    }

    /**
     * Stop the webcamera - stop refreshing the snapshot.
     */
    public void stopWebCamera(){
        timer.cancel();
        timer.purge();
    }
}

