package tiberius.tiberius;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Handler;
import android.os.Looper;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;

/**
 * Thread class to handle the Socket for the Database pi unit.
 */
public class DatabaseThread implements Runnable {

    // GLOBAL VARIABLES & PARAMETERS

    // The PORT of the control socket.
    private final static int CONTROL_PORT = 60000;
    // Check for x ms before throwing a TIMETOUT
    private final static int TIMEOUT = 3000;

    // COMMANDS TO SEND TO THE DATABASE
    private final static String WRITE = "WRITE";
    private final static String READ  = "READ";
    // mode commands
    private final static String AUTONOMY_MODE = "AUTONOMY_MODE"; // mission_start
    private final static String MANUAL_MODE   = "MANUAL_MODE";
    private final static String IDLE_MODE     = "IDLE_MODE";     // mission_stop
    // current status of the mission
    private final static String MISSION_STATUS = "MISSION_STATUS";
    // mission commands
    private final static String MISSION_START       = "MISSION_START";
    private final static String MISSION_PAUSED      = "MISSION_PAUSED";
    private final static String MISSION_RESUMED     = "MISSION_RESUMED";
    private final static String DESTINATION_REACHED = "DESTINATION_REACHED";
    private final static String OBJECT_DETECTED     = "OBJECT_DETECTED";
    // mission parameters
    private final static String MISSION_GPS    = "MISSION_GPS";
    private final static String MISSION_OBJECT = "MISSION_OBJECT";
    // sensor parameters
    private final static String GPS     = "GPS";
    private final static String COMPASS = "COMPASS";
    private final static String LIDAR   = "LIDAR";
    // object similarity parameters
    private final static String OBJECT_SIMILARITY = "OBJECT_SIMILARITY";

    // The socket used to send data to the control unit.
    private Socket  socket;

    // The context of the activity that called the thread.
    private Context context;

    // The IP address of the database unit.
    private String database_IP;

    // Constructor
    public DatabaseThread(Context context, String IP) {
       this.context = context;
       this.database_IP = IP;
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
            SocketAddress socketAddress = new InetSocketAddress(database_IP, CONTROL_PORT);

            socket.connect(socketAddress, TIMEOUT);

            // while the socket isn't closed, get the latest database values (every 500ms).
            while(!socket.isClosed()){
                getDatabaseValues();
            }

        } catch (UnknownHostException e) {} //not implemented
        // If the socket can't connect to the control unit, display an alert and return to the main menu.
        catch (IOException e) {

            // If mission is stopped, display the unable to connect alert.
            if (new Autonomy().missionStopped()){
                connectionUnavailableAlert();
            }
            // If mission is not stopped, display the connection has been dropped alert.
            else{
                connectionLostAlert();
            }
        }
    }

    /**
     * Send the start manual mode command to the database unit.
     */
    public void setManualMode(){
        // Output message format : "WRITE.MANUAL_MODE."
        String message = WRITE + "." + MANUAL_MODE + ".";
        sendMessage(message);
    }

    /**
     * Send the idle command to the database unit - stops either autonomy or manual mode.
     */
    public void setIdleMode(){
        // Output message format : "WRITE.IDLE_MODE."
        String message = WRITE + "." + IDLE_MODE + ".";
        sendMessage(message);
    }

    /**
     * Send the autonomy mode command (start mission) to the database unit along with the GPS destination and object to be detected.
     */
    public void setAutonomyMode(String latitude, String longitude, String object){
        // Output message format : "WRITE.AUTONOMY_MODE,LAT:latitude,LON:longitude,OBJ:object.
        String message = WRITE + "." + AUTONOMY_MODE + ",LAT:" + latitude + ",LON:" + longitude + ",OBJ:" + object + ".";
        sendMessage(message);
    }

    /**
     * Send the start mission command to the database unit.
     */
    public void startMission(){
        // Output message format : "WRITE.MISSION_STATUS,MISSION_START."
        String message = WRITE + "." + MISSION_STATUS + "," + MISSION_START + ".";
        sendMessage(message);
    }

    /**
     * Send the pause mission command to the database unit.
     */
    public void pauseMission(){
        // Output message format : "WRITE.MISSION_STATU,MISSION_PAUSED."
        String message = WRITE + "." + MISSION_STATUS + "," + MISSION_PAUSED + ".";
        sendMessage(message);
    }

    /**
     * Send the resume mission command to the database unit.
     */
    public void resumeMission(){
        // Output message format : "WRITE.MISSION_STATUS,MISSION_RESUMED."
        String message = WRITE + "." + MISSION_STATUS + "," + MISSION_RESUMED + ".";
        sendMessage(message);
    }

    /**
     * Get the current status of the mission.
     */
    public String getMissionStatus(){
        // Output message format: "READ.MISSION_STATUS."
        String message = READ + "." + MISSION_STATUS + ".";
        sendMessage(message);

        return receiveMessage();
    }

    /**
     * Check with the database whether the mission is paused.
     */
    public boolean missionPaused(){
        // Output message format: "READ.MISSION_PAUSED."
        String message = READ + "." + MISSION_PAUSED  + ".";
        sendMessage(message);

        String received = receiveMessage(); // receive from database

        if(received.equals("TRUE")){
            return true;
        }
        else return false;
    }

    /**
     * Get the mission GPS parameters from the database.
     */
    public String getMissionGPS(){
        // Output message format: "READ.MISSION_GPS."
        String message = READ + "." + MISSION_GPS  + ".";
        sendMessage(message);

        // Retrieved message format: "LATITUDE_VALUE,LONGITUDE_VALUE"
        return receiveMessage();
    }

    /**
     * Get the mission object from the database.
     */
    public String getMissionObject(){
        // Output message format: "READ.MISSION_OBJECT."
        String message = READ + "." + MISSION_OBJECT  + ".";
        sendMessage(message);

        return receiveMessage();
    }

    /**
     * Get the current GPS location from the database.
     * Data format: "LATITUDE_VALUE,LONGITUDE_VALUE"
     */
    public String getGPSData(){
        // Output message format: "READ.GPS."
        String message = READ + "." + GPS  + ".";
        sendMessage(message);

        return receiveMessage();
    }

    /**
     * Get the current compass heading from the database.
     * Data format: "COMPASS_VALUE
     */
    public String getCompassData(){
        // Output message format: "READ.COMPASS."
        String message = READ + "." + COMPASS  + ".";
        sendMessage(message);

        return receiveMessage();
    }

    /**
     * Get the current lidar data from the database.
     * Data format: "(LINE_1)START_ANGLE,START_DISTANCE,END_ANGLE,END_DISTANCE,(LINE_2)START_ANGLE,START_DISTANCE,..."
     */
    public String getLidarData(){
        // Output message format: "READ.LIDAR."
        String message = READ + "." + LIDAR  + ".";
        sendMessage(message);

        return receiveMessage();
    }

    /**
     * Get the object matches similarity from the database.
     */
    public String getObjectSimilarity(){
        // Output message format: "READ.OBJECT_SIMILARITY."
        String message = READ + "." + OBJECT_SIMILARITY  + ".";
        sendMessage(message);

        // Retrieved message format: "CUBE_VALUE,HEXAGON_VALUE,STAR_VALUE"
        return receiveMessage();
    }

    /**
     * Send a message to the database unit.
     */
    private void sendMessage(String message){
        try {
            // Get the outputstream of the socket.
            PrintWriter output = new PrintWriter(socket.getOutputStream());

            // JAVA appends an EOL character (\n) at the end of the String. Python won't recognise this.
            message = message.replaceAll("\n", "");

            // Send the message via the socket.
            output.print(message);
            output.flush();

            // If the connection to the database unit has been dropped, pause the mission, display an alert and return to the main menu.
            if (output.checkError()) {
                connectionLostAlert();
            }
        }
        catch (IOException e) {} //not implemented
    }

    /**
     * Receive a message from the database unit.
     */
    private String receiveMessage(){
        try {
            // Get the inputstream of the socket.
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            // Receive the message via the socket.
            String received_message = input.readLine();

            // If the connection has been dropped, send N/A.
            if(received_message == null){
                return "N/A";
            }
            else{
                return received_message;
            }

        }
        catch (IOException e) {
            return "N/A";
        }
    }

    /**
     * Get the latest database values and update all the relevant fields every 500 ms.
     */
    private void getDatabaseValues(){

        try {
            // Sleep for 500ms before fetching the new database values.
            Thread.sleep(500);

            // Update the mission status in the Autonomy activity.
            String mission_status = getMissionStatus();
            new Autonomy().setMissionState(mission_status);

            // Update the status of the compass.
            String compass = getCompassData();
            new Database().setCompass(compass);

            // Update the status of the GPS.
            String gps_location = getGPSData();
            //ERROR CATCHING
            if (gps_location.equals("N/A")) {
                gps_location = gps_location.concat(",N/A");
            }
            // Split the gps_location into latitude and longitude
            final String gps_parts[] = gps_location.split(",");
            new Database().setLatitude(gps_parts[0]);
            if (gps_parts.length > 1) {
                new Database().setLongitude(gps_parts[1]);
            }

            // Check whether any mission milestones have been reached.
            checkMissionMilestone(mission_status, gps_parts);

            // Sleep for 500ms before fetching the lidar data.
            Thread.sleep(500);

            // Update the status of the lidar.
            String lidar_data = getLidarData();
            new Database().setLidar(lidar_data);
        }
        catch(InterruptedException e){}
    }

    /**
     * Check whether any mission milestones have been reached.
     */
    private void checkMissionMilestone(String mission_status, final String gps_parts[]) {

        // If a mission is running.
        if (!new Autonomy().missionStopped()) {

            /*  DESTINATION_REACHED  */
            if (mission_status.equals(DESTINATION_REACHED)) {

                new Handler().post(new Runnable() {
                    @Override
                    public void run() {
                        // MISSION OBJECT HAS BEEN SELECTED - MISSION CONTINUES
                        if (new MissionSelection().objectSelected()) {
                            AlertDialog.Builder builder = new AlertDialog.Builder(context);
                            builder.setTitle("DESTINATION REACHED!");
                            builder.setMessage("Tiberius has reached its destination!\n\n" +
                                    "--------------------------------------------------------------------------------------------------\n" +
                                    "GPS location:     LATITUDE : " + gps_parts[0]  + "\n" +
                                    "                          LONGITUDE : " + gps_parts[1] + "\n");
                            builder.setCancelable(false);
                            // if OK, move on to scan for the mission object.
                            builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    // Re-start the intent to exit the looper.loop.
                                    closeSocket();
                                    Intent intent = new Intent(context, context.getClass());
                                    context.startActivity(intent);
                                }
                            });
                            builder.show(); // Display the alert.
                        }
                        // NO MISSION OBJECT HAS BEEN SELECTED - MISSION FINISHED
                        else {
                            AlertDialog.Builder builder = new AlertDialog.Builder(context);
                            builder.setTitle("MISSION COMPLETED!");
                            builder.setMessage("Tiberius has reached its destination!\n\n" +
                                    "--------------------------------------------------------------------------------------------------\n" +
                                    "GPS location:     LATITUDE : " + gps_parts[0] + "\n" +
                                    "                          LONGITUDE : " + gps_parts[1] + "\n\n" +
                                    "--------------------------------------------------------------------------------------------------\n\n" +
                                    "The mission has completed!\nWould you like to start a new mission?");
                            builder.setCancelable(false);
                            // if YES, stop the mission and go the mission selection activity.
                            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    new Autonomy().stopMission();
                                    closeSocket();
                                    Intent intent = new Intent(context, MissionSelection.class);
                                    context.startActivity(intent);
                                }
                            });
                            // if NO, stop the mission and go the main menu activity.
                            builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    new Autonomy().stopMission();
                                    setIdleMode();
                                    closeSocket();
                                    Intent intent = new Intent(context, MainMenu.class);
                                    context.startActivity(intent);
                                }
                            });
                            builder.show(); // Display the alert.
                        }
                    }
                });
                Looper.loop();
            }
            /*  OBJECT_DETECTED  */
            else if (mission_status.equals(OBJECT_DETECTED)) {

                // OBJECT MATCHES SIMILARITY
                String similarity = getObjectSimilarity();
                final String similarity_parts [] = similarity.split(",");

                new Handler().post(new Runnable() {
                    @Override
                    public void run() {
                        AlertDialog.Builder builder = new AlertDialog.Builder(context);
                        builder.setTitle("MISSION COMPLETED!");
                        builder.setMessage("Tiberius has detected: " + new MissionSelection().getObject() + "!\n\n" +
                                "--------------------------------------------------------------------------------------------------\n" +
                                "GPS location:     LATITUDE : " + gps_parts[0]  + "\n" +
                                "                          LONGITUDE : " + gps_parts[1] + "\n\n" +
                                "Similarity Results:          CUBE : " + similarity_parts[0] + "%\n" +
                                "                                  HEXAGON : " + similarity_parts[1] + "%\n" +
                                "                                           STAR : " + similarity_parts[2] + "%\n" +
                                "--------------------------------------------------------------------------------------------------\n\n" +
                                "The mission has completed!\nWould you like to start a new mission?");
                        builder.setCancelable(false);
                        // if YES, stop the mission and go the mission selection activity.
                        builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                closeSocket();
                                Intent intent = new Intent(context, MissionSelection.class);
                                context.startActivity(intent);
                            }
                        });
                        // if NO, stop the mission and go the main menu activity.
                        builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                new Autonomy().stopMission();
                                setIdleMode();
                                closeSocket();
                                Intent intent = new Intent(context, MainMenu.class);
                                context.startActivity(intent);
                            }
                        });
                        builder.show(); // Display the alert.
                    }
                });
                Looper.loop();
            }
        }
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
                builder.setMessage("Connection unavailable!\nTiberius won't be able to receive any status updates.\n\n" +
                                   "Please check the status of the database unit and make sure " +
                                   "that you have set the correct IP address in the Settings.");
                builder.setCancelable(false);
                builder.setIcon(R.drawable.alert_icon);
                builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // AUTONOMY
                        if (context instanceof Autonomy) {
                            new Autonomy().getWebCamera().stopWebCamera();
                        }
                        // MANUAL
                        else if (context instanceof Manual){
                            new Manual().getWebCamera().stopWebCamera();
                        }
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
    public void connectionLostAlert(){
        // Close the socket.
        closeSocket();

        // Create a handler that displays the alert from the thread on the UI.
        new Handler().post(new Runnable() {
            @Override
            public void run() {

                // If the running activity is not Manual.
                if (!(context instanceof Manual)) {
                    AlertDialog.Builder builder = new AlertDialog.Builder(context);
                    builder.setTitle("Connection Dropped!");
                    String message = "Whoops! Seems like the connection has been dropped.\n" +
                            "Please check the status of the database unit." ;
                    if(!new Autonomy().missionStopped()){
                        message = message.concat("\n\nThe current mission will be stopped.");
                    }
                    builder.setMessage(message);
                    builder.setCancelable(false);
                    builder.setIcon(R.drawable.alert_icon);
                    // if YES, stop the current mission and return to the main menu.
                    builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // AUTONOMY
                            if(context instanceof Autonomy) {
                                new Autonomy().getWebCamera().stopWebCamera();
                            }
                            // AUTONOMY & MAIN MENU & SETTINGS & DATABASE
                            new Autonomy().stopMission();
                            setIdleMode();
                            Intent intent = new Intent(context, MainMenu.class);
                            context.startActivity(intent);
                        }
                    });
                    builder.show(); // Display the alert.
                }
                // Else if the running activity is Manual.
                else{
                    AlertDialog.Builder builder = new AlertDialog.Builder(context);
                    builder.setTitle("Connection Dropped!");
                    builder.setMessage("Whoops! Seems like the connection has been dropped.\n" +
                            "Please check the status of the database unit.\n\n" +
                            "Leaving manual mode.");
                    builder.setCancelable(false);
                    builder.setIcon(R.drawable.alert_icon);
                    // Press OK to acknowledge the message.
                    builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                        }
                    });
                    builder.show(); // Display the alert.
                }
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
