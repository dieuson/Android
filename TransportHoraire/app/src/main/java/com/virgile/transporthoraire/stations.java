package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import org.json.JSONObject;

/**
 * Created by dieuson on 2/16/17.
 */

public class stations extends Activity {

    protected String[] get_stations(JSONObject json)
    {
        String[] tab = null;


        return tab;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.stations);

        Intent get_dir_res = getIntent();
        String json_str = get_dir_res.getStringExtra("json");
        String direction = get_dir_res.getStringExtra("destination");
        String stations = null;

    }
}
