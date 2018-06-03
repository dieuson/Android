package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

/**
 * Created by dieuson on 2/20/17.
 */

public class affichage extends Activity {

    private String getMessage(JSONObject json) throws JSONException {
        String response_str = json.getString("response");
        json = new JSONObject(response_str);
        JSONArray jsonarray = json.getJSONArray("schedules");
        String message = jsonarray.getString(0);
        json = new JSONObject(message);
        message = json.getString("message");
//        Log.i("DJAYYMESSAGE", message);
        return message;
    }

    private void displayData(String name, String station, String destination, String message)
    {
        TextView arret = (TextView)findViewById(R.id.arret);
        TextView heure = (TextView)findViewById(R.id.heure);
        TextView dest = (TextView)findViewById(R.id.destination);

        arret.setText(station);
        heure.setText(message);
        name = name.replace("/", "");
        dest.setText(name + " direction " + destination);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.affichage);

        Intent getval = getIntent();
        String url = getval.getStringExtra("url");
        String mode = getval.getStringExtra("mode");
        String lineName = getval.getStringExtra("name");
        String destination = getval.getStringExtra("destination");
        String destinationName = getval.getStringExtra("destinationName");
        String stationsName = getval.getStringExtra("stationName");
        String stationsId = getval.getStringExtra("stationId");
        String urlToParse = url + mode + lineName + "stations/" + stationsId + "?destination=" + destination;
        String message = null;
        DownloadData data = new DownloadData();
        try {
            Log.i("DJAYYURL", urlToParse);
            String jsonStr = data.execute(urlToParse).get();
            message = getMessage(new JSONObject(jsonStr));
            displayData(lineName, stationsName, destinationName, message);

        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
