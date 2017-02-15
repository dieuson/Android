package com.virgile.transporthoraire;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

/**
 * Created by dieuson on 2/7/17.
 */

public class linenumber extends Activity {
    Button bouton_valider = null;
    EditText line_number = null;
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.linenumber);

        line_number = (EditText)findViewById(R.id.line_number);
        bouton_valider = (Button)findViewById(R.id.bouton_suivant1);

        bouton_valider.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String text_line_number = line_number.getText().toString();
                if (text_line_number.isEmpty() || !text_line_number.matches("^[0-9]+$"))
                {
                    Context context = getApplicationContext();
                    CharSequence text = "Entrez uniquement des nombres";
                    Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
                    toast.setMargin(-1, 0);
                    toast.show();
                    return;
                }
                MainActivity.url_to_parse += text_line_number + "/";
                Intent display_layout = new Intent(linenumber.this, directionchoice.class);
                startActivity(display_layout);
            }
        });

    }
}
