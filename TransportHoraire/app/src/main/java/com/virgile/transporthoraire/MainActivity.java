package com.virgile.transporthoraire;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;

import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    RadioButton radio_bus;
    RadioButton radio_rer;
    RadioButton radio_metro;
    RadioButton radio_tram;
    Button bouton_valider;
    String type = null;

    String url_to_parse = "http://api-ratp.pierre-grimaud.fr/v2/";
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        radio_bus = (RadioButton)findViewById(R.id.bus);
        radio_rer = (RadioButton)findViewById(R.id.rer);
        radio_metro = (RadioButton)findViewById(R.id.metro);
        radio_tram = (RadioButton)findViewById(R.id.tram);
        bouton_valider = (Button)findViewById(R.id.bouton_suivant2);

        radio_bus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                radio_rer.setChecked(false);
                radio_metro.setChecked(false);
                radio_tram.setChecked(false);
            }
        });
        radio_rer.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                radio_bus.setChecked(false);
                radio_metro.setChecked(false);
                radio_tram.setChecked(false);
            }
        });
        radio_metro.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                radio_rer.setChecked(false);
                radio_bus.setChecked(false);
                radio_tram.setChecked(false);
            }
        });
        radio_tram.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                radio_rer.setChecked(false);
                radio_metro.setChecked(false);
                radio_bus.setChecked(false);
            }
        });
        bouton_valider.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (radio_bus.isChecked())
                    type = "bus/";
                else if (radio_rer.isChecked())
                    type = "rers/";
                else if (radio_tram.isChecked())
                    type = "tramways/";
                else if (radio_metro.isChecked())
                    type = "metros/";
                else
                {
                    Context context = getApplicationContext();
                    CharSequence text = "Choisit un de ces moyen de transport";
                    int duration = Toast.LENGTH_SHORT;
                    Toast toast = Toast.makeText(context, text, duration);
                    toast.show();
                    return ;
                }
                Intent switch_layou = new Intent(MainActivity.this, linenumber.class);
                switch_layou.putExtra("url", url_to_parse);
                switch_layou.putExtra("mode", type);
                startActivity(switch_layou);

            }
        });
    }
}
