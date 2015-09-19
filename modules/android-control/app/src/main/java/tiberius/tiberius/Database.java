package tiberius.tiberius;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Looper;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.text.Html;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.TextView;
import java.util.Timer;
import java.util.TimerTask;


/**
 * DATABASE ACTIVITY
 */
public class Database extends ActionBarActivity {

    // GLOBAL VARIABLES & PARAMETERS

    // Compass - directions
    private final static String NORTH = "\nN";
    private final static String SOUTH = "\nS";
    private final static String WEST  = "\nW";
    private final static String EAST  = "\nE";
    private final static String NORTH_WEST = "\nNW";
    private final static String NORTH_EAST = "\nNE";
    private final static String SOUTH_WEST = "\nSW";
    private final static String SOUTH_EAST = "\nSE";
    // Angle symbol
    private final static char ANGLE = (char) 0x00B0;
    // Compass text field space - just for alignment
    private final static String SPACE = "\n  ";

    // The compass field value - initialised to N/A.
    private static String compass = "N/A";
    // The latitude and longitude field values - initialised to N/A.
    private static String latitude  = "N/A";
    private static String longitude = "N/A";
    // The lidar data value - initialised to 0.
    private static String lidar_data = "0";

    // Lidar SurfaceView dimensions.
    private final static float X_MAX    = 530;
    private final static float Y_MAX    = 450;
    private final static float X_MIDDLE = X_MAX/2;
    private final static float Y_MIDDLE = Y_MAX/2;

    // The lidar's maximum range point.
    private final static float LIDAR_RANGE = 600;

    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    // Timer object to control the communication with the database unit.
    private Timer timer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_database);

        // Create the socket thread for communicating with the databse.
        final String database_IP = new SettingsMenu().getDatabaseIP();
        database_thread = new DatabaseThread(Database.this,database_IP);
        new Thread(database_thread).start();

        // Update the database fields every 200ms.
        updateDatabaseFields();

        // Format the headings.
        TextView textView = (TextView) findViewById(R.id.database_gps);
        textView.setText(Html.fromHtml("<u>GPS:</u>"));
        textView = (TextView) findViewById(R.id.database_compass_label);
        textView.setText(Html.fromHtml("<u>COMPASS:</u>"));
        textView = (TextView) findViewById(R.id.database_lidar_label);
        textView.setText(Html.fromHtml("<u>LIDAR:</u>"));
   }

    /**
     * Update the database fields every 200ms.
     */
    private void updateDatabaseFields(){
        timer = new Timer();

        //Textviews
        final TextView text_latitude  = (TextView) findViewById(R.id.database_latitude);
        final TextView text_longitude = (TextView) findViewById(R.id.database_longitude);
        final TextView text_compass   = (TextView) findViewById(R.id.database_compass);

        // LIDAR
        SurfaceView surfaceView = (SurfaceView) findViewById(R.id.lidar);
        final SurfaceHolder lidar_holder = surfaceView.getHolder();

        TimerTask timerTask = new TimerTask() {

            @Override
            public void run() {
                Database.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        text_latitude.setText(getLatitude());
                        text_longitude.setText(getLongitude());
                        text_compass.setText(decodeCompassData());

                        // LIDAR - DRAW CANVAS
                        Canvas canvas = lidar_holder.lockCanvas();
                        if(canvas != null) {
                            drawLidar(canvas);
                            lidar_holder.unlockCanvasAndPost(canvas);
                        }

                    }
                });
            }
        };
        // Schedule the fields to be updated every 200ms.
        timer.schedule(timerTask, 0, 200);
    }

    /**
     * Set the latitude field value.
     */
    public void setLatitude(String latitude){
        this.latitude = latitude;
    }

    /**
     * Get the latitude field value.
     */
    private String getLatitude() {
        return this.latitude;
    }

    /**
     * Set the longitude field value.
     */
    public void setLongitude(String longitude){
        this.longitude = longitude;
    }

    /**
     * Get the longitude field value.
     */
    private String getLongitude() {
        return this.longitude;
    }

    /**
     * Set the compass field value.
     */
    public void setCompass(String compass){
        this.compass = compass;
    }

    /**
     * Get the compass field value.
     */
    private String getCompass() {
        return this.compass;
    }

    /**
     * Set the lidar data value.
     */
    public void setLidar(String lidar_data){
        this.lidar_data = lidar_data;
    }

    /**
     * Get the lidar data value.
     */
    private String getLidar() {
        return this.lidar_data;
    }

    /**
     * Decode the compass value and return the string to display.
     */
    private String decodeCompassData(){

        // DEFAULT - RETURN "N/A"
        if(getCompass().equals("N/A")){
            return "\nN/A";
        }

        else{
            float heading_value = Float.parseFloat(getCompass());
            // NORTH
            if (heading_value < 25 || heading_value >= 335) {
                return SPACE + getCompass() + ANGLE + NORTH;
            }
            // NORTH EAST
            else if (heading_value >= 25 && heading_value < 65) {
                return SPACE + getCompass() + ANGLE + NORTH_EAST;
            }
            // EAST
            else if (heading_value >= 65 && heading_value < 115) {
                return SPACE + getCompass() + ANGLE + EAST;
            }
            // SOUTH EAST
            else if (heading_value >= 115 && heading_value < 155) {
                return SPACE + getCompass() + ANGLE + SOUTH_EAST;
            }
            // SOUTH
            else if (heading_value >= 155 && heading_value < 205) {
                return SPACE + getCompass() + ANGLE + SOUTH;
            }
            // SOUTH WEST
            else if (heading_value >= 205 && heading_value < 245) {
                return SPACE + getCompass() + ANGLE + SOUTH_WEST;
            }
            // WEST
            else if (heading_value >= 245 && heading_value < 295) {
                return SPACE + getCompass() + ANGLE + WEST;
            }
            // NORTH WEST
            else if (heading_value >= 295 && heading_value < 335) {
                return SPACE + getCompass() + ANGLE + NORTH_WEST;
            }
            // VALUE out of range
            else{
                return "\nN/A";
            }
        }
    }

    /**
     * Draw the current lidar data on the canvas.
     */
    private void drawLidar(Canvas lidar_canvas){

        // Initialise LIDAR view - Make it White.
        lidar_canvas.drawRGB(255,255,255);

        // Paint parameters for the robot
        Paint robot_paint = new Paint();
        robot_paint.setStrokeWidth(10);
        robot_paint.setStyle(Paint.Style.FILL_AND_STROKE);
        robot_paint.setColor(Color.GREEN);

        // Add the robot point in the middle of the canvas.
        lidar_canvas.drawPoint(X_MIDDLE, Y_MIDDLE, robot_paint);

        // Paint parameters for the objects.
        Paint lidar_paint = new Paint();
        lidar_paint.setStrokeWidth(5);
        lidar_paint.setStyle(Paint.Style.FILL_AND_STROKE);
        lidar_paint.setColor(Color.RED);

        // Get the decoded lidar data.
        float [] lidar_data = decodeLidarData();

        // Draw each line from the lidar data.
        for(int i=0; i < lidar_data.length-1; i = i+4){
            //i = i + 4 => because a line is defined by 4 values: x_start,y_start,x_end,y_end
            // x_start = lidar_data[i], y_start = lidar_data[i+1], x_end = lidar_data[i+2], y_end = lidar_data[i+3]
            lidar_canvas.drawLine(lidar_data[i],lidar_data[i+1],lidar_data[i+2],lidar_data[i+3],lidar_paint);
        }
    }

    /**
     * Decode Lidar Data and return the list of lines found.
     * Original Data has the format: "(LINE_1)START_ANGLE,START_DISTANCE,END_ANGLE,END_DISTANCE,(LINE_2)START_ANGLE,START_DISTANCE,..."
     * Decoded  List has the format: "(LINE_1)X_START,Y_START,X_END,Y_END,(LINE_2)X_START,Y_START,..."
     */
    private float[] decodeLidarData(){

        String lidar_data_string = getLidar();

        // If there is any lidar data.
        if(!lidar_data_string.equals("WRITE.LIDAR,EMPTY.")) {

            // Split the lidar data in its values and store them in a list.
            String lidar_data_array[] = lidar_data_string.split(",");

            // Get the number of points in the lidar data.
            int lidar_data_length = lidar_data_array.length;

            // Check if the data received is not complete - e.g. expecting 16 points but received 15.
            if (lidar_data_length%4 != 4){
                // Get the number of extra points and subtract these points to get a functional data set.
                int extra_points = lidar_data_length%4;
                lidar_data_length = lidar_data_length - extra_points;
            }

            // Convert the values from String to float.
            float lidar_data[] = new float[lidar_data_length];

            for (int i = 0; i < lidar_data_length - 1; i = i + 2) {
                float angle = Float.parseFloat(lidar_data_array[i]);
                float distance = Float.parseFloat(lidar_data_array[i + 1]);

                // Subtract 90 degrees from the angle to align it to the y direction.
                angle = angle - 90;

                // If there is compass data, compensate for the difference between the compass domain and the actual
                // domain. The compass angle is added to the actual angle before being sent to the database.
                if (!getCompass().equals("N/A")) {
                    angle = angle - Float.parseFloat(getCompass());
                }

                // Compensate if  the angle is more than 360 degrees.
                if (angle > 360) {
                    angle = angle - 360;
                }

                // Compensate if the angle is less than 0 degrees.
                else if (angle < 0) {
                    angle = 360 + angle;
                }

                // Convert the data from polar to rectangular coordinates.
                // Point x
                float x = distance * (float) Math.cos(angle * 2 * Math.PI / 360);
                lidar_data[i] = adjustX(x);
                // Point y
                float y = distance * (float) Math.sin(angle * 2 * Math.PI / 360);
                lidar_data[i + 1] = adjustY(y);
            }

            return lidar_data;
        }

        // If there isn't any lidar data, return an empty array.
        else{
            float lidar_data [] = new float[0];
            return lidar_data;
        }
    }

    /**
     * Adjust the X direction of the lidar data.
     */
    private float adjustX(float x){
        float x_adjusted;

        // Scale the lidar value down - The lidar can work up to 6 meters from the center point.
        // If 1px -> 1cm, then 600px -> 600cm. Our limit is 265px from the center point.
        x_adjusted = (x/LIDAR_RANGE) * X_MIDDLE;

        // The lidar's reference point is (265,225).
        // The surface's reference point is (0,0). We adjust this to match the lidar's reference point.
        x_adjusted = X_MIDDLE + x_adjusted;

        return x_adjusted;
    }

    /**
     * Adjust the Y direction of the lidar data.
     */
    private float adjustY(float y){
        float y_adjusted;

        // Scale the lidar value down - The lidar can work up to 6 meters from the center point.
        // If 1px -> 1cm, then 600px -> 600cm. Our limit is 225px from the center point.
        y_adjusted = (y/LIDAR_RANGE) * Y_MIDDLE;

        // The lidar's reference point is (265,225).
        // The surface's reference point is (0,0). We adjust this to match the lidar's reference point.
        y_adjusted = Y_MIDDLE - y_adjusted;

        // The Y direction goes from 0px at the top to 450 at the bottom.
        // We adjust the value so that the point (0,0) is at the bottom left corner of the view.
        y_adjusted = Y_MAX - y_adjusted;

        return y_adjusted;
    }

    /**
     * Called when the user presses the menu button
     * Move to the Main Menu activity.
     */
    public void goMenu(View view) {
        timer.cancel();
        timer.purge();
        database_thread.closeSocket();
        this.goMainMenu();
    }

    /**
     * Go to the Main Menu.
     */
    private void goMainMenu(){
        Intent intent = new Intent(this,MainMenu.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the back button
     * Move to the Main Menu activity.
     */
    @Override
    public void onBackPressed() {
        timer.cancel();
        timer.purge();
        database_thread.closeSocket();
        this.goMainMenu();
    }

    /**
     * Called when the user leaves the activity.
     */
    @Override
    protected void onPause() {
        super.onPause();
        timer.cancel();
        timer.purge();

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

        // Update the database fields every 200ms.
        updateDatabaseFields();

        // Format the headings.
        TextView textView = (TextView) findViewById(R.id.database_gps);
        textView.setText(Html.fromHtml("<u>GPS:</u>"));
        textView = (TextView) findViewById(R.id.database_compass_label);
        textView.setText(Html.fromHtml("<u>COMPASS:</u>"));
        textView = (TextView) findViewById(R.id.database_lidar_label);
        textView.setText(Html.fromHtml("<u>LIDAR:</u>"));

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
