package tiberius.tiberius;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioGroup;

/**
 * MISSION SELECTION ACTIVITY
 */
public class MissionSelection extends ActionBarActivity {

    // GLOBAL VARIABLES & PARAMETERS

    // GPS Coordinates
    private static String latitude  = "";
    private static String longitude = "";

    // MISSION OBJECTS
    private final static String CUBE    = "CUBE";
    private final static String HEXAGON = "HEXAGON";
    private final static String STAR    = "STAR";
    private final static String NONE    = "NONE";

    // SELECTED MISSION OBJECT (Initially no object)
    private static String object = NONE;

    // The thread handling the socket for sending commands to the database unit.
    private DatabaseThread database_thread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mission_selection);

        // Set the last selected latitude and longitude.
        EditText edit_latitude  = (EditText) findViewById(R.id.mission_selection_latitude);
        edit_latitude.setText(getLatitude());
        EditText edit_longitude = (EditText) findViewById(R.id.mission_selection_longitude);
        edit_longitude.setText(getLongitude());

        // Set the last selected object.
        RadioGroup object_group = (RadioGroup) findViewById(R.id.mission_selection_objects);
        object_group.check(getObjectID());

        // Create the socket thread for the autonomy mode.
        String database_IP = new SettingsMenu().getDatabaseIP();
        database_thread = new DatabaseThread(MissionSelection.this,database_IP);
        new Thread(database_thread).start();
    }

    /**
     * Get the GPS latitude.
     */
    public String getLatitude(){
        return this.latitude;
    }

    /**
     * Set the GPS latitude.
     */
    public void setLatitude(String latitude){
        this.latitude = latitude;
    }

    /**
     * Get the GPS longitude.
     */
    public String getLongitude(){
        return this.longitude;
    }

    /**
     * Set the GPS longitude.
     */
    public void setLongitude(String longitude) {
        this.longitude = longitude;
    }

    /**
     * Get the Mission Object.
     */
    public String getObject() {
        return this.object;
    }

    /**
     * Set the Mission Object.
     */
    public void setObject(String object) {
        this.object = object;
    }

    /**
     * Get the selected Mission Object's ID.
     */
    private int getObjectID() {
        // MISSION OBJECTS ID
        int cube_id     = R.id.mission_selection_cube;
        int hexagon_id  = R.id.mission_selection_hexagon;
        int star_id     = R.id.mission_selection_star;
        int none        = -1; // no object is selected from the objects_group

        // CUBE
        if(getObject().equals(CUBE)) {
            return cube_id;
        }
        // HEXAGON
        else if (getObject().equals(HEXAGON)) {
            return hexagon_id;
        }
        // STAR
        else if(getObject().equals(STAR)) {
            return star_id;
        }
        // NO OBJECT
        else{
            return none;
        }
    }

    /**
     * Get the Mission Object's icon ID.
     */
    public int getObjectIconID() {

        // MISSION OBJECTS ICON
        int cube_icon     = R.drawable.cube;
        int hexagon_icon  = R.drawable.hexagon;
        int star_icon     = R.drawable.star;
        int no_object     = R.drawable.no_object;

        // CUBE
        if(getObject().equals(CUBE)) {
            return cube_icon;
        }
        // HEXAGON
        else if (getObject().equals(HEXAGON)) {
            return hexagon_icon;
        }
        // STAR
        else if(getObject().equals(STAR)) {
            return star_icon;
        }
        // NO OBJECT
        else{
            return no_object;
        }
    }

    /**
     * Called when the user presses the map button.
     * Opens GOOGLE MAPS and allows user to choose his destination point.
     */
    public void goMap(View view){
        Intent intent = new Intent(this, ChooseDestination.class);
        startActivity(intent);
    }

    /**
     * Called when the user presses the apply button.
     * Displays an alert message before starting the mission.
     */
    public void applyMissionSelection(View view) {

        // LATITUDE
        EditText edit_latitude = (EditText) findViewById(R.id.mission_selection_latitude);
        String selected_latitude  = edit_latitude.getText().toString();
        // LONGITUDE
        EditText edit_longitude = (EditText) findViewById(R.id.mission_selection_longitude);
        String selected_longitude  = edit_longitude.getText().toString();

        // OBJECT
        RadioGroup object_group = (RadioGroup) findViewById(R.id.mission_selection_objects);
        final String object = decodeObjectID(object_group.getCheckedRadioButtonId());

        //Check if the provided latitude and longitude are valid.
        if(validLatitude(selected_latitude) == false){
            invalidLatitudeAlert(selected_latitude);
        }

        else if(validLongitude(selected_longitude) == false) {
            invalidLongitudeAlert(selected_longitude);
        }

        // Else, if an object has been selected.
        else if(!object.equals(NONE)) {

            // Round the GPS parameters to 6 decimal points.
            final String latitude = roundGPSParameter(selected_latitude);
            final String longitude = roundGPSParameter(selected_longitude);

            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("New Mission");
            builder.setMessage("Are you sure you want to start a mission with the following settings?\n\n" +
                    "Latitude = \"" + latitude + "\"\nLongitude = \"" + longitude + "\"\nObject = \"" + object + "\"");
            builder.setCancelable(false);

            // If "YES" pressed, send the mission parameters, start the mission and return to the Autonomy menu.
            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    setLatitude(latitude);
                    setLongitude(longitude);
                    setObject(object);

                    // send start command to the database - latitude, longitude, object.
                    database_thread.setAutonomyMode(getLatitude(),getLongitude(),getObject());
                    new Autonomy().startMission();
                    database_thread.closeSocket();
                    Intent intent = new Intent(MissionSelection.this, Autonomy.class);
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

        // Else, ask if the mission should be started without searching for an object.
        else {

            // Round the GPS parameters to 6 decimal points.
            final String latitude = roundGPSParameter(selected_latitude);
            final String longitude = roundGPSParameter(selected_longitude);

            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("New Mission");
            builder.setMessage("No object has been selected! Tiberius will not look for an object during this mission.\n\n" +
                               "Are you sure you want to start a mission with the following settings?\n\n" +
                               "Latitude = \"" + latitude + "\"\nLongitude = \"" + longitude + "\"");
            builder.setCancelable(false);

            // If "YES" pressed, send the mission parameters, start the mission and return to the Autonomy menu.
            builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    setLatitude(latitude);
                    setLongitude(longitude);
                    setObject(object);

                    // send start command to the database - latitude, longitude, no_object.
                    database_thread.setAutonomyMode(getLatitude(),getLongitude(),getObject());
                    database_thread.startMission();
                    database_thread.closeSocket();
                    new Autonomy().startMission();
                    Intent intent = new Intent(MissionSelection.this, Autonomy.class);
                    startActivity(intent);
                }
            });

            // If "NO" pressed, make no changes.
            builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {}});

            builder.show(); // Display the alert.
        }
    }

    /**
     * Decode the selected object's ID into its String format.
     */
    private String decodeObjectID(int object_id){

        // MISSION OBJECTS ICON ID
        int cube_icon_id     = R.id.mission_selection_cube;
        int hexagon_icon_id  = R.id.mission_selection_hexagon;
        int star_icon_id     = R.id.mission_selection_star;

        // CUBE
        if(cube_icon_id == object_id) {
            return CUBE;
        }
        // HEXAGON
        else if (hexagon_icon_id == object_id) {
            return HEXAGON;
        }
        // STAR
        else if(star_icon_id == object_id) {
            return STAR;
        }
        // NO OBJECT
        else{
            return NONE;
        }
    }

    /**
     * Check if the provided latitude is valid.
     */
    private boolean validLatitude(String latitude){
        String valid_latitude = "^((\\-|\\+)?\\d{1,2})(\\.\\d+)?$";

        // If the latitude doesn't match the valid_latitude pattern, return false.
        if(latitude.matches(valid_latitude) == false){
            return false;
        }

        // If the latitude is more than 90 or less than - 90, return false.
        else if((Float.parseFloat(latitude) > 90) || (Float.parseFloat(latitude) < -90)){
            return false;
        }

        // Else, the latitude is valid.
        else{
            return true;
        }
    }

    /**
     * Check if the provided longitude is valid.
     */
    private boolean validLongitude(String longitude){
        String valid_longitude = "^((\\-|\\+)?\\d{1,3})(\\.\\d+)?$";

        // If the longitude doesn't match the valid_longitude pattern, return false.
        if(longitude.matches(valid_longitude) == false){
            return false;
        }

        // If the longitude is more than 180 or less than - 180, return false.
        else if((Float.parseFloat(longitude) > 180) || (Float.parseFloat(longitude) < -180)){
            return false;
        }

        // Else, the longitude is valid.
        else{
            return true;
        }
    }

    /**
     * Display an invalid latitude alert.
     */
    private void invalidLatitudeAlert(String latitude){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("ERROR!");
        builder.setMessage("Invalid latitude: " + latitude + "! \n\n Please provide a latitude from 0 to (+/-) 90 in 6 decimal degrees.");
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
     * Display an invalid longitude alert.
     */
    private void invalidLongitudeAlert(String longitude){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("ERROR!");
        builder.setMessage("Invalid longitude: " + longitude + "! \n\n Please provide a longitude from 0 to (+/-) 180 in 6 decimal degrees.");
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
     * Round the GPS parameter to 6 decimal places.
     */
    private String roundGPSParameter(String parameter){

        double param_double = Double.parseDouble(parameter);

        // Round to 6 decimal places
        param_double = (double) Math.round(param_double * 1000000) / 1000000;

        parameter = Double.toString(param_double);

        // Split the parameter into 2 strings based on the location of the decimal point.
        String parts[] = parameter.split("\\.");

        // Find the length of the fractional part. Append necessary 0's to reach a length of 6.
        for (int i=parts[1].length(); i < 6; i++){
            parameter = parameter.concat("0");
        }

        return parameter;
    }

    /**
     * Called when the user pressed the None button.
     * Unchecks the selected object.
     */
    public void cancelObjectSelection(View view){
        RadioGroup object_group  = (RadioGroup) findViewById(R.id.mission_selection_objects);
        object_group.clearCheck();
    }

    /**
     * Returns whether the current mission has an object selected.
     */
    public boolean objectSelected(){
        if(getObject().equals(NONE)){
            return false;
        }
        else return true;
    }

    /**
     * Called when the user presses the cancel button.
     * Returns to the Autonomy activity without choosing any mission parameters.
     */
    public void cancelMissionSelection(View view) {
        onBackPressed();
    }

    /**
     * Called when the user presses the back button.
     * Move to the Autonomy activity.
     */
    @Override
    public void onBackPressed() {
        database_thread.closeSocket();
        Intent intent = new Intent(this,Autonomy.class);
        startActivity(intent);
    }
}
