package com.example.dieuson.myapplication;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.view.View.OnClickListener;
import android.view.inputmethod.InputMethodManager;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    RelativeLayout layout = null;
    EditText taille = null;
    EditText poids = null;
    Button bouton_calc = null;
    Button bouton_raz = null;
    TextView displ_area = null;
    RadioButton cm_button = null;
    RadioButton metres_button = null;
    ImageView image_imc = null;
    float imc = 0f;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        layout = (RelativeLayout) RelativeLayout.inflate(this, R.layout.activity_main, null);



        cm_button = (RadioButton) layout.findViewById(R.id.cm);
        metres_button = (RadioButton) layout.findViewById(R.id.metres);
        image_imc = (ImageView) layout.findViewById(R.id.tab_imc);

        taille = (EditText) layout.findViewById(R.id.taille);
        poids = (EditText) layout.findViewById(R.id.poids);
        displ_area = (TextView) layout.findViewById(R.id.Resultat);

        bouton_calc = (Button) layout.findViewById(R.id.button_calcul);
        image_imc.setVisibility(View.INVISIBLE);
        cm_button.setChecked(true);
        metres_button.setChecked(false);
        bouton_calc.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                imm.hideSoftInputFromWindow(bouton_calc.getWindowToken(), 0);
                if (taille.getText().length() <= 0 || poids.getText().length() <= 0) {
                    displ_area.setText("Veuillez entrer des valeurs");
                    return;
                }

                float val_taille = Float.valueOf(taille.getText().toString());
                if (metres_button.isChecked()) {
                    val_taille *= 100;
                }
                float val_poids = Float.valueOf(poids.getText().toString());
                val_taille = val_taille / 100;
                imc = val_poids / (val_taille * val_taille);
                image_imc.setVisibility(View.VISIBLE);
                displ_area.setText(String.format("%.2f", imc));
            }
        });
        bouton_raz = (Button) layout.findViewById(R.id.bouton_reset);
        bouton_raz.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                taille.getText().clear();
                poids.getText().clear();
                image_imc.setVisibility(View.INVISIBLE);
                displ_area.setText(null);
            }
        });
        cm_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                metres_button.setChecked(false);
            }
        });
        metres_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                cm_button.setChecked(false);
            }
        });
        setContentView(layout);
    }
    @Override
    public void onClick(View v) {


    }
}
