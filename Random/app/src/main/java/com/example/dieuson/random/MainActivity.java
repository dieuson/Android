package com.example.dieuson.random;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    Button six_faces_dice = null;
    Button twenty_faces_dice = null;
/* MENU
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.xml_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.first_elem:
                setContentView("FIRST ELEM");
                return true;
            case R.id.second_elem:
                setContentView("SECOND ELEM");
                return true;
            case R.id.third_elem:
                setContentView("THIRD ELEM");
                return  true;
            default:
                return  super.onOptionsItemSelected(item);
        }
    }
*/
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        six_faces_dice = (Button)findViewById(R.id.button_six_faces);
        twenty_faces_dice = (Button)findViewById(R.id.button_twenty_faces);
        six_faces_dice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myintent = new Intent(MainActivity.this, roll_the_dice.class);
                myintent.putExtra("max", 6);
                myintent.putExtra("type", getString(R.string.d_a_six_faces));
                startActivity(myintent);
            }
        });
        twenty_faces_dice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myintent = new Intent(MainActivity.this, roll_the_dice.class);
                myintent.putExtra("max", 20);
                myintent.putExtra("type", getString(R.string.d_a_vingt_faces));
                startActivity(myintent);
            }
        });
    }


    public void setContentView(String text) {
        six_faces_dice = (Button)findViewById(R.id.button_six_faces);
        six_faces_dice.setText(text);
    }
}
