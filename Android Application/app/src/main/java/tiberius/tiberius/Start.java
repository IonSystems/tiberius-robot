package tiberius.tiberius;

import android.content.Intent;
import android.graphics.Canvas;
import android.graphics.Rect;
import android.media.MediaPlayer;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.VideoView;

import java.io.IOError;
import java.io.IOException;

/**
 *  START UP ACTIVITY - play an introduction video.
 */
public class Start extends ActionBarActivity{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);

     /*   SurfaceView surfaceView = (SurfaceView) findViewById(R.id.start_video);
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
                mediaPlayer.release();*/
                Intent intent = new Intent(Start.this, MainMenu.class);
                startActivity(intent);
            }
 //       });
 //   }
}
