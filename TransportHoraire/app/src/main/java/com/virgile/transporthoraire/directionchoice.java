package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Intent;
import android.database.CharArrayBuffer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
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
            String[] response = new String[4];
            String destination_1 = null;
            String destination_2 = null;
            String destination_id_1 = null;
            String destination_id_2 = null;
            try {
                String response_str = json.getString("response");
                json = new JSONObject(response_str);
                JSONArray test_array = json.getJSONArray("destinations");
                destination_1 = test_array.getJSONObject(0).getString("destination");
                destination_2 = test_array.getJSONObject(1).getString("destination");
                destination_id_1 = test_array.getJSONObject(0).getString("id_destination");
                destination_id_2 = test_array.getJSONObject(1).getString("id_destination");
                response[0] = destination_1;
                response[1] = destination_id_1;
                response[2] = destination_2;
                response[3] = destination_id_2;
                return response;
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String[] result) {
            RadioButton destination_a = (RadioButton)findViewById(R.id.destinationA);
            RadioButton destination_b = (RadioButton)findViewById(R.id.destinationB);
            destination_a.setText(result[0]);
            destination_b.setText(result[2]);
            super.onPostExecute(result);
        }
    }
    String[] tab_tmp = new String[4];
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.directionchoice);
        String url_direction = MainActivity.url_to_parse;
        final String[] id_direction = {null};

        TextView disp_result = (TextView)findViewById(R.id.test);
        final RadioButton destination_a = (RadioButton)findViewById(R.id.destinationA);
        final RadioButton destination_b = (RadioButton)findViewById(R.id.destinationB);
        Button valider = (Button)findViewById(R.id.bouton_suivant2);

        destination_a.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (destination_a.isChecked() == true)
                    destination_b.setChecked(false);
        //        if (tab_tmp[2] != null)
          //          id_direction[0] = tab_tmp[2];
            }
        });
        destination_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (destination_b.isChecked() == true)
                    destination_a.setChecked(false);
      //          if (tab_tmp[0] != null)
    //                id_direction[0] = tab_tmp[4];
            }
        });

        valider.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent go_selection_stations = new Intent(directionchoice.this, stations.class);
                if (destination_a.isChecked() || destination_b.isChecked())
                {
                    go_selection_stations.putExtra("destination", id_direction);
                    startActivity(go_selection_stations);
                }
            }
        });
        disp_result.setText(url_direction);
        DownloadData data = new DownloadData();
        try {
            String str = data.execute(url_direction).get();
            try {
                JSONObject json = new JSONObject(str);
                get_sens fill_buttons = new get_sens();
                tab_tmp = fill_buttons.execute(json).get();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }


    }

}
