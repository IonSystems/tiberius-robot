package tiberius.tiberius;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;

public class MainMenuActivity extends ActionBarActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);

    }

    public void goManual(View view){
        Intent intent = new Intent(this, ThumbControlActivity.class);
        startActivity(intent);
    }

    public void goDatabase(View view){
        Intent intent = new Intent(this, DatabaseActivity.class);
        startActivity(intent);
    }

    public void goSettings(View view){
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
    }

    public void goWASDControl(View view){
        Intent intent = new Intent(this, WASDControlActivity.class);
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
    }

    /**
     * Called when the user re-enters the activity (used for re-entering the application).
     */
    @Override
    protected void onRestart() {
        super.onRestart();

    }
}
