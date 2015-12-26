package tiberius.tiberius;

/**
 * A class for setting the speed of a motor based on a seekbar.
 * It is called in the Manual.java class.
 */
public class Motor {

    /** GLOBAL VARIABLES & PARAMETERS */

    // PROGRESS BAR GOES FROM {0,510}
    // THAT IS TRANSLATED INTO {-255,+255} for the motor (-Reverse, +Forward)
    // The speed adjustment to scale from {0,510} to {-255,+255}.
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
    public Motor(String id){
        this.id = id;
    }

    /**
     * Stop the motor
     */
    public void stopMotor() {
        this.speed = STOP;
    }

    /**
     * Set the speed of the motor
     */
    public void setSpeed(int speed) {
        this.speed = speed + SPEED_ADJUSTMENT;
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
