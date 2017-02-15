package com.example.dieuson.random;

import android.app.Activity;
import android.content.Intent;
import android.media.Image;
import android.os.CountDownTimer;
import android.support.annotation.DrawableRes;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.Random;
import java.util.logging.Handler;
import java.util.logging.LogRecord;

public class roll_the_dice extends Activity {

    TextView result_roll = null;
    Button button_roll = null;
    TextView type_de_de = null;
    ImageView contain_dice = null;
    String type = null;
    int max = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_roll_the_dice);

        max = getIntent().getIntExtra("max", 0);
        type = getIntent().getStringExtra("type");

        type_de_de = (TextView)findViewById(R.id.type_lance);
        result_roll = (TextView)findViewById(R.id.result_roll);
        button_roll = (Button)findViewById(R.id.button_roll);
        contain_dice = (ImageView)findViewById(R.id.show_dice);

        if (max > 6)
            result_roll.setVisibility(View.VISIBLE);
        type_de_de.setText(type);
        button_roll.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new CountDownTimer(1000, 50){
                    int result_random = 0;
                    int dice_choiced = 0;
                    Random r = new Random();
                    @Override
                    public void onTick(long millisUntilFinished) {
                        result_random = r.nextInt(max) + 1;
                        dice_choiced = 2130903040;
                        dice_choiced += result_random % 6;
                        if (max == 6)
                            contain_dice.setBackgroundResource(dice_choiced);
                        else
                            result_roll.setText(String.valueOf(result_random));
                    }

                    @Override
                    public void onFinish() {

                    }
                }.start();
            }
        });
    }
}
