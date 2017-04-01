package tiberius.tiberius;

import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.preference.PreferenceManager;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;


public class StartupActivity extends ActionBarActivity{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);
        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(getBaseContext());
        boolean show_video = SP.getBoolean("startup_video", false);
        if(show_video) {
            Log.d("STARTUP_PLAYER","Playing startup video.");
            SurfaceView surfaceView = (SurfaceView) findViewById(R.id.start_video);
            SurfaceHolder surfaceHolder = surfaceView.getHolder();

            // The video to be played.
            final MediaPlayer mediaPlayer = MediaPlayer.create(this,R.raw.starting_page);

            // Check when the surface is created,changed and destroyed.
            surfaceHolder.addCallback(new SurfaceHolder.Callback() {
                // When the surface is created, start the video.
                @Override
                public void surfaceCreated(SurfaceHolder holder) {
                    mediaPlayer.start();
                    mediaPlayer.setDisplay(holder);
                }

                @Override
                public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

                }

                @Override
                public void surfaceDestroyed(SurfaceHolder holder) {

                }
            });

            // When the video is completed, release any resources and go to the main menu.
            mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                @Override
                public void onCompletion(MediaPlayer mp) {
                    mediaPlayer.reset();
                    mediaPlayer.release();
                    Intent intent = new Intent(StartupActivity.this, MainMenuActivity.class);
                    startActivity(intent);
                }
            });
        }else{
            Log.d("STARTUP_PLAYER","Skipping startup video.");
            Intent intent = new Intent(StartupActivity.this, MainMenuActivity.class);
            startActivity(intent);
        }

    }
}
