package com.virgile.transporthoraire;

import android.os.AsyncTask;

import org.json.JSONObject;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import android.os.AsyncTask;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by root on 2/7/17.
 */

public class DownloadData extends AsyncTask<String,Void,String>
{
    static public String result_text = null;
    static JSONObject result_json = null;
    @Override
    protected String doInBackground(String... urls) {
        String result = "";
        URL url;
        HttpURLConnection urlConnection = null;
        try {
            url = new URL(urls[0]);
            urlConnection = (HttpURLConnection)url.openConnection();

            InputStream in = urlConnection.getInputStream();
            InputStreamReader reader = new InputStreamReader(in);

            int data = reader.read();
            while (data != -1)
            {
                char current = (char) data;
                result += current;
                data = reader.read();
            }
            result_text = result;
            return  result;
        }
        catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    protected void onPostExecute(String result) {
        super.onPostExecute(result);
        try {
            JSONObject jsonObject = new JSONObject(result);
            result_json = jsonObject;
//            JSONObject weatherData = new JSONObject(jsonObject.getString("main"));

  //          Double temperature = Double.parseDouble(weatherData.getString("temp"));

      //      int temperatureInteger = (int) (temperature * 1.8 - 459.67);

    //        String place = jsonObject.getString("name");

//            MainActivity.temperatureTextView.setText(String.valueOf(temperatureInteger));
            //          MainActivity.placeTextView.setText(place);

        } catch (Exception e) {
            e.printStackTrace();
        }


    }
}
