package com.virgile.eat4share

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_home.*

class HomeActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        rateYourMealIB!!.setOnClickListener {
            val intent = Intent(this, RateYourMealActivity::class.java)
            startActivity(intent)
        }

        historyIB!!.setOnClickListener {
            val intent = Intent(this, HistoryActivity::class.java)
            startActivity(intent)
        }

        findYourMealIB!!.setOnClickListener {
            val intent = Intent(this, FindYourMealActivity::class.java)
            startActivity(intent)
        }
    }
}
