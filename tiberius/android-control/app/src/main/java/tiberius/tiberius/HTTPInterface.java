package tiberius.tiberius;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.http.AndroidHttpClient;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.Looper;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.net.ssl.HttpsURLConnection;


public class HTTPInterface {

    HashMap<String, String> params;
    String left_speed;
    String right_speed;

    String ip_address;

    Context context;

    HTTPInterface(Context context, String ip_address){

        this.params = new HashMap();
        this.left_speed = "0";
        this.right_speed = "0";
        this.ip_address = ip_address;

        this.context = context;
    }

    /**
     * Update the text field with the speed value.
     */
    protected String sendSpeeds(Integer... speed) {

        params.put("left_speed", left_speed);
        params.put("right_speed", right_speed);
        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(this.context);
        String api_token = SP.getString("x_auth_token", "DEFAULTPASSWORDTHATWONTWORK");
        params.put("X-Auth Token", api_token);
        Log.d("API", "Sending (" + this.ip_address + ")left: " + left_speed + ", right: " + right_speed);

        return performAndroidPostCall("http://" + this.ip_address + "/motors", params);
//        return performPostCall("http://" + this.ip_address + "/motors", params);
    }

    public String performAndroidPostCall(String request_url,  HashMap<String, String> postDataParams) {

        Log.d("HTTP-A", "Start request");
        AndroidHttpClient client = null;
        client = AndroidHttpClient.newInstance(userAgent(), this.context);
        HttpPost request = new HttpPost(request_url);

        ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
        Iterator it = postDataParams.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry pair = (Map.Entry)it.next();
            nameValuePairs.add(new BasicNameValuePair(pair.getKey().toString(), pair.getValue().toString()));
            it.remove(); // avoids a ConcurrentModificationException
        }


        try {
            request.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = client.execute(request);
            StatusLine statusLine = response.getStatusLine();
            Log.d("HTTP-A", "status code: " + statusLine.getStatusCode());
            //Log.d("HTTP-A", "Response: " + response.getParams());
            client.close();
        }catch(UnsupportedEncodingException e){
            Log.e("HTTP-A", "Unsupported Encoding Exception");
        } catch (IOException e) {
            Log.e("HTTP-A", "IO Exception");
        }
        return "";
    }

    private String userAgent() {
        String userAgent = null;
        if (userAgent != null) {
        }
        if (userAgent == null) {
            userAgent = "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13";
        }
        return userAgent;
    }
    public String  performPostCall(String requestURL,
                                   HashMap<String, String> postDataParams) {
        long startTime = System.currentTimeMillis();


        URL url;
        String response = "";
        try {
            url = new URL(requestURL);
        }catch(MalformedURLException e) {
            Log.e("HTTP", "Request failed: Malformed URL");
            return "";
        }
        HttpURLConnection conn;
        try {
           conn = (HttpURLConnection) url.openConnection();
            conn.setReadTimeout(15000);
            conn.setConnectTimeout(1000);
            //conn.setRequestMethod("POST");
            conn.setDoInput(true);
            conn.setDoOutput(true);
        }catch(ProtocolException e){
            Log.e("HTTP", "Request failed: Bad protocol");
            return "";
        }catch(IOException e){
            Log.e("HTTP", "Request failed: IO Exception");
            return "";
        }



            OutputStream os;
        try {
            os = conn.getOutputStream();
        }catch(IOException e){
            Log.e("HTTP", "Request failed: IO Exception 2");
            return "";
        }
            BufferedWriter writer;
        try {
            writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(getPostDataString(postDataParams));

            writer.flush();
            writer.close();
            os.close();
            int responseCode=conn.getResponseCode();

            if (responseCode == HttpsURLConnection.HTTP_OK) {
                String line;
                BufferedReader br=new BufferedReader(new InputStreamReader(conn.getInputStream()));
                while ((line=br.readLine()) != null) {
                    response+=line;
                }
            }
            else {
                response="";

            }

        }catch(UnsupportedEncodingException e){
            Log.e("HTTP", "Request failed: Unsupported encoding");
            return "";
        }catch(IOException e){
            Log.e("HTTP", "Request failed: IO Exception 3");
            return "";
        }

        long stopTime = System.currentTimeMillis();
        long elapsedTime = stopTime - startTime;
        System.out.println(elapsedTime + " ms");

        return response;
    }

    private String getPostDataString(HashMap<String, String> params) throws UnsupportedEncodingException {
        StringBuilder result = new StringBuilder();
        boolean first = true;
        for(Map.Entry<String, String> entry : params.entrySet()){
            if (first)
                first = false;
            else
                result.append("&");

            result.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
            result.append("=");
            result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
        }

        return result.toString();
    }

    private void connectionError(){
        connectionUnavailableAlert();
    }

    private void connectionUnavailableAlert(){

        Looper.prepare();
        // Create a handler that displays the alert from the thread on the UI.
        new Handler().post(new Runnable() {
            @Override
            public void run() {
                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                builder.setTitle("Unable to Connect!");
                builder.setMessage("Connection unavailable!\nPlease check the status of the control unit and make sure " +
                        "that you have set the correct IP address in the Settings.");
                builder.setCancelable(false);
                builder.setIcon(R.drawable.alert_icon);
                builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Intent intent = new Intent(context, MainMenuActivity.class);
                        context.startActivity(intent);
                    }
                });
                builder.show(); // Display the alert.
            }
        });
        // Loop until the button is pressed.
        Looper.loop();
    }
}