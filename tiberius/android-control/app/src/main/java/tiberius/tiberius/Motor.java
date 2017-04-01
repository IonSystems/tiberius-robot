package tiberius.tiberius;

import android.util.Log;

/**
 * A class for setting the speed of a motor based on a seekbar.
 * It is called in the ThumbControlActivity.java class.
 */
public class Motor {

    private int min_speed_seekbar;
    private int max_speed_seekbar;

    private final static int SPEED_ADJUSTMENT = -255;

    // SPEED = 0 => MOTOR STOPPED
    private final static int STOP = 0;

    // SPEED OF THE MOTOR - initially stopped
    private int speed = STOP;

    // MOTOR ID
    private String id = "";

    /**
     * Constructor
     */
    public Motor(String id, int min_speed_seekbar, int max_speed_seekbar){
        this.id = id;
        this.min_speed_seekbar = min_speed_seekbar;
        this.max_speed_seekbar = max_speed_seekbar;

    }

    /**
     * Stop the motor
     */
    public void stopMotor() {
        this.speed = STOP;
    }

    /**
     * The speed comes in with a a range of 0 --> 200.
     * We store this as a normalised speed -100 to 100.
     */
    public void setSpeed(int speed) {
        //Represent the speed as a percentage ( 0 --> 1)
        double percentage = ((double)speed - (double)this.min_speed_seekbar) / ((double)this.max_speed_seekbar - (double)this.min_speed_seekbar);
        //Convert the percentage into a valid range for API (-100 --> 100)
        int speed_api =  (int) Math.round(((percentage - 0.5) / 0.5) * 100);
        this.speed = speed_api;
    }

    /**
     * Get the speed of the motor
     */
    public int getSpeed() {
        return this.speed;
    }

    /**
     * Set the ID of the motor
     */
    public void setID(String new_id) {
        this.id  = new_id;
    }

    /**
     * Get the ID of the motor
     */
    public String getID() {
        return this.id;
    }
}
