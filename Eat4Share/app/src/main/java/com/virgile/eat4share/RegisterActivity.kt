package com.virgile.eat4share

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.text.TextUtils
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_register.*

class RegisterActivity : AppCompatActivity() {

    private var userName: String? = null
    private var userEmail: String? = null
    private var userToken: String? = null
    private var registerMode: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        userName = intent.getStringExtra(ARG_USER_NAME)
        userEmail = intent.getStringExtra(ARG_EMAIL)
        userToken = intent.getStringExtra(ARG_TOKEN)
        registerMode = intent.getStringExtra(ARG_REGISTER_MODE)

        submitRegisterBtn.setOnClickListener { checkRegisterFields() }
        initInputs()
    }

    private fun initInputs() {
        val intent = intent

        /*Set datas extracts from previous activity*/
        userNameET.setText(userName)
        userEmailET.setText(userEmail)
    }

    private fun launchHomeAcivity() {
        val intent = Intent(this, HomeActivity::class.java)
        startActivity(intent)
    }

    private fun checkRegisterFields(): Boolean {
        var errors = 0
        if (TextUtils.isEmpty(userNameET.text.toString())) {
            userNameET.error = "champ obligatoire"
            if (errors == 0)
                userNameET.callOnClick()
            errors += 1
        }
        if (TextUtils.isEmpty(userEmailET.text.toString())) {
            userEmailET.error = "champ obligatoire"
            if (errors == 0)
                userEmailET.callOnClick()
            errors += 1
        }

        if (TextUtils.isEmpty(passwordET.text.toString())) {
            passwordET.error = "champ obligatoire"
            if (errors == 0)
                userNameET.callOnClick()
            errors += 1
        }
        if (TextUtils.isEmpty(confirmPasswordET.text.toString())) {
            confirmPasswordET.error = "champ obligatoire"
            if (errors == 0)
                confirmPasswordET.callOnClick()
            errors += 1
        }

        if (passwordET.text.toString() != confirmPasswordET.text.toString()) {
            Toast.makeText(this, "Les mots de passe ne sont pas identiques", Toast.LENGTH_LONG).show()
            if (errors == 0)
                passwordET.callOnClick()
            errors += 1
        }

        if (errors == 0) {
            launchHomeAcivity()
            return true
        } else {
            val toast = Toast.makeText(baseContext, R.string.register_fields_empty, Toast.LENGTH_SHORT)
            toast.show()
            return false
        }
    }

    companion object {
        private val ARG_USER_REGISTER_DATA = "user_register_data"
        private val ARG_USER_NAME = "userName"
        private val ARG_EMAIL = "email"
        private val ARG_TOKEN = "token"
        private val ARG_REGISTER_MODE = "register_mode"

        fun newIntent(context: Context, hash: HashMap<String, Any>): Intent {
            val intent = Intent(context, this.javaClass)
            intent.putExtra(ARG_USER_REGISTER_DATA, hash)
            return intent
        }
    }

}
