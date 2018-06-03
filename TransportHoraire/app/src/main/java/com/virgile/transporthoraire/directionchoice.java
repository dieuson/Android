package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

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
                destination_id_1 = test_array.getJSONObject(0).getString("slug");
                destination_id_2 = test_array.getJSONObject(1).getString("slug");
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
    String direction = null;
    String directionName = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.directionchoice);
        Intent get_val = getIntent();
        String url_direction = get_val.getStringExtra("url") + get_val.getStringExtra("mode") + get_val.getStringExtra("name");

        TextView disp_result = (TextView)findViewById(R.id.test);
        final RadioButton destination_a = (RadioButton)findViewById(R.id.destinationA);
        final RadioButton destination_b = (RadioButton)findViewById(R.id.destinationB);
        Button valider = (Button)findViewById(R.id.bouton_suivant2);
        String str = null;

        disp_result.setText(url_direction);
        DownloadData data = new DownloadData();
        try {
            str = data.execute(url_direction).get();
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

        destination_a.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (destination_a.isChecked() == true)
                    destination_b.setChecked(false);
                direction = tab_tmp[1];
                directionName = tab_tmp[0];
            }
        });
        destination_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (destination_b.isChecked() == true)
                    destination_a.setChecked(false);
                direction = tab_tmp[3];
                directionName = tab_tmp[2];
            }
        });

        final String finalStr = str;
        valider.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (destination_a.isChecked() || destination_b.isChecked())
                {
                    Intent go_selection_stations = new Intent(directionchoice.this, stations.class);
                    Intent get_val = getIntent();

                    go_selection_stations.putExtra("destination", direction);
                    go_selection_stations.putExtra("destinationName", directionName);
                    go_selection_stations.putExtra("json", finalStr);

                    go_selection_stations.putExtra("url", get_val.getStringExtra("url"));
                    go_selection_stations.putExtra("mode", get_val.getStringExtra("mode"));
                    go_selection_stations.putExtra("name", get_val.getStringExtra("name"));
                    startActivity(go_selection_stations);
                }
            }
        });


    }

}
