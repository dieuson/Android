package com.virgile.transporthoraire;

import android.app.Activity;
import android.database.CharArrayBuffer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.RadioButton;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutionException;

import javax.net.ssl.HttpsURLConnection;

/**
 * Created by dieuson on 2/7/17.
 */

public class directionchoice extends Activity {

    public class get_sens extends AsyncTask<JSONObject, Void, String[]>{
        @Override
        protected String[] doInBackground(JSONObject... params) {
            JSONObject json = params[0];
            String[] response = null;
            String destination_1 = null;
            String destination_2 = null;
            if (json == null)
                Log.i("DJAYY", "JSON NULL");
            Log.i("DJAYY", json.toString());
            try {
                String response_str = json.getString("destinations");
                Log.i("DJAYY", "1");
                Log.i("DJAYY", response_str);
                json = new JSONObject(response_str);
                Log.i("DJAYY", "2");
                Log.i("DJAYY", json.toString());
                json = json.getJSONObject("destinations");
                Log.i("DJAYY", "3");
                Log.i("DJAYY", json.toString());

                JSONArray test_array = json.getJSONArray("destinations");
                Log.i("DJAYY", "4");
                Log.i("DJAYY", test_array.getJSONObject(0).toString());



//                JSONArray test_array = json.getJSONArray("destinations");
                destination_1 = test_array.getJSONObject(0).getString("destination");
                destination_2 = test_array.getJSONObject(1).getString("destination");

                Log.i("DJAYY", destination_1);
                Log.i("DJAYY", destination_2);
                response[0] = destination_1;
                response[1] = destination_2;
                return response;
            } catch (JSONException e) {
                e.printStackTrace();
                Log.i("DJAYY", "ELSE");
            }
            return null;
        }

        @Override
        protected void onPostExecute(String[] result) {
            RadioButton destination_a = (RadioButton)findViewById(R.id.destinationA);
            RadioButton destination_b = (RadioButton)findViewById(R.id.destinationB);

            destination_a.setText("toto");
            if (result != null && result[0] != null)
                destination_b.setText(result[0]);
            super.onPostExecute(result);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.directionchoice);
        String url_direction = MainActivity.url_to_parse;
        String destination_1 = "";
        String destination_2 = "";

        TextView disp_result = (TextView)findViewById(R.id.test);
        RadioButton destination_a = (RadioButton)findViewById(R.id.destinationA);
        RadioButton destination_b = (RadioButton)findViewById(R.id.destinationB);

        Log.i("DJAYY", "IN DIRECTIONCHOICE");
        String result = null;
        disp_result.setText(url_direction);
        Log.i("DJAYY", "URL TO PARSE");
        Log.i("DJAYY", url_direction);
        DownloadData data = new DownloadData();
        try {
            data.execute(url_direction).get();
            JSONObject json = data.result_json;
            get_sens test = new get_sens();
            test.execute(json);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }


    }

}
