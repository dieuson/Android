package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.ScrollView;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Created by dieuson on 2/19/17.
 */

public class stations extends Activity{

    private String[] getValues (Bundle intent)
    {
        String destination = intent.getString("destination");
        String jsonStr = intent.getString("json");
        String[] stringArray = new String[2];
        stringArray[0] = destination;
        stringArray[1] = jsonStr;
        return stringArray;
    }

    private String[][] getStations(String s) {
        String[][] stationArray = null;
        try {
            JSONObject json = new JSONObject(s);
            String response_str = json.getString("response");
            json = new JSONObject(response_str);
            JSONArray jsonarray = json.getJSONArray("stations");
            JSONObject jsonInfos = null;
            stationArray = new String[jsonarray.length()][];
            for (int i=0; i < jsonarray.length(); i++)
            {
                jsonInfos = jsonarray.getJSONObject(i);
                String[] stationLine = new String[2];
                stationLine[0] = jsonInfos.getString("name");
                stationLine[1] = jsonInfos.getString("slug");
                stationArray[i] = stationLine;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return  stationArray;
    }

    private void createRadioButtons(final String[][] stationsArray){
        LinearLayout layout = new LinearLayout(this);
        ScrollView scroll = new ScrollView(this);
        for (int i=0; i < stationsArray.length; i++)
        {
            Button btnTag = new Button(this);
            btnTag.setLayoutParams(new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT));
            btnTag.setId(i);
            btnTag.setText(stationsArray[i][0]);
            btnTag.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
            final int finalI = i;
            btnTag.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String name = stationsArray[finalI][0];
                    String id = stationsArray[finalI][1];
                    Intent intent = new Intent(stations.this, affichage.class);
                    Intent getval = getIntent();
                    intent.putExtra("url", getval.getStringExtra("url"));
                    intent.putExtra("mode", getval.getStringExtra("mode"));
                    intent.putExtra("name", getval.getStringExtra("name"));
                    intent.putExtra("destination", getval.getStringExtra("destination"));
                    intent.putExtra("destinationName", getval.getStringExtra("destinationName"));
                    intent.putExtra("stationName", name);
                    intent.putExtra("stationId", id);
                    startActivity(intent);
                }
            });
            layout.setGravity(Gravity.CENTER);
            layout.setOrientation(LinearLayout.VERTICAL);
            layout.addView(btnTag);
        }
        scroll.addView(layout);
        setContentView(scroll);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.stations);
        String[] stringsArray = getValues(getIntent().getExtras());
        String destination = stringsArray[0];
        String stationsStr = stringsArray[1];
        try {
            String[][] stationsArray = null;
            stationsArray = getStations(stationsStr);
            createRadioButtons(stationsArray);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
