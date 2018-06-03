/**
 *  Created by VIRGILE_dieuson on 03/01/2017
 */

package com.virgile.weather;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.DatePicker;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URLConnection;
import java.net.URL;


import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends AppCompatActivity {
    RelativeLayout layout = null;
    DatePicker date1 = null;
    ImageView visu1 = null;
    data toto = new data();

    String link = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris&units=metric&cnt=5&appid=8194ea842a9aef80a798c8ac0c320ec4";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        layout = (RelativeLayout) RelativeLayout.inflate(this, R.layout.activity_main, null);
        visu1 = (ImageView) layout.findViewById(R.id.visu1);
        TextView temp1 = (TextView) layout.findViewById(R.id.temp1);
        link = "https://www.google.fr/search?q=mkyong&gws_rd=cr&ei=QStwWOynIoW0acT9h6gI";
        link = "file:///home/dieuson/Desktop/data.json";
        toto.city = "salut";


        try {
            URL obj = new URL(link);
            BufferedReader reader = new BufferedReader(new InputStreamReader(obj.openStream()));
            StringBuffer buffer = new StringBuffer();
            int read;
            System.out.println("\nSending 'GET' request to URL : ");
//            char[] chars = new char[1024];
  //          while ((read = reader.read(chars)) != -1) {
    //            buffer.append(chars, 0, read);
      //      }
       //     toto.city = buffer.toString();

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

//        new JSONTask().execute(link);
//        toto.doInBackground(link);


        temp1.setText(toto.city);
//        temp1.setText(test);
        setContentView(layout);
    }
}

