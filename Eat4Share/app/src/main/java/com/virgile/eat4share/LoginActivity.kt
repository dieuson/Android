package com.virgile.eat4share

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.facebook.*
import com.facebook.login.LoginResult
import com.twitter.sdk.android.core.*
import com.twitter.sdk.android.core.identity.TwitterAuthClient
import kotlinx.android.synthetic.main.activity_login.*
import kotlinx.android.synthetic.main.activity_register.*
import org.json.JSONObject
import java.util.*
import kotlin.collections.HashMap

class LoginActivity : Activity() {

    private lateinit var callbackManager: CallbackManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Twitter.initialize(this)
        FacebookSdk.sdkInitialize(applicationContext)
        callbackManager = CallbackManager.Factory.create()
        setContentView(R.layout.activity_login)

        testRegister.setOnClickListener {
            val intent = Intent(baseContext, HistoryActivity().javaClass)
            startActivity(intent)
        }

        twitterLoginButton!!.callback = object : Callback<TwitterSession>() {
            override fun success(resultConnection: Result<TwitterSession>) {
                /*On success twitter connection*/
                val session = TwitterCore.getInstance().sessionManager.activeSession
                val authToken = session.authToken
                val authClient = TwitterAuthClient()
                authClient.requestEmail(session, object : Callback<String>() {
                    override fun success(resultEmailRequest: Result<String>) {
                        /*On success twitter return User email*/
                        val hash = HashMap<String, Any>()
                        hash.put("userId", resultConnection.data.userId)
                        hash.put("token", authToken.token)
                        hash.put("secret", authToken.secret)
                        hash.put("userName", resultConnection.data.userName)
                        hash.put("email", resultEmailRequest.data)
                        hash.put("register_mode", "twitter")

                        launchRegisterActivity(hash)
                    }

                    override fun failure(exception: TwitterException) {
                        /*Fail to get user emai*/
                        Log.i("Login", "Twitter get email fail")
                        val toast = Toast.makeText(baseContext, R.string.login_fail_get_email, Toast.LENGTH_LONG)
                        toast.show()
                    }
                })
            }

            override fun failure(exception: TwitterException) {
                /*Fail to log in twitter account*/
                Log.i("Login", "Twitter Log fail")
                val toast = Toast.makeText(baseContext, R.string.login_fail_get_email, Toast.LENGTH_LONG)
                toast.show()
            }
        }

        facebookLoginButton!!.setReadPermissions(Arrays.asList("email", "user_birthday"))
        facebookLoginButton!!.registerCallback(callbackManager, object : FacebookCallback<LoginResult> {
            override fun onSuccess(loginResult: LoginResult) {
                /*Success connection to facebook account*/
                val parameters = Bundle()
                /*Datas we want to extract from facebook user account*/
                parameters.putString("fields", "id, email, gender, birthday")
                GraphRequest(AccessToken.getCurrentAccessToken(),
                        "/" + loginResult.accessToken.userId,
                        parameters,
                        HttpMethod.GET,
                        GraphRequest.Callback { response ->
                            /* All data are loaded let's register*/

                            val jsonObject = JSONObject().getJSONObject(response.toString())
                            val hash = HashMap<String, Any>()
                            hash.put("username", jsonObject.get("name").toString())
                            hash.put("email", jsonObject.get("email").toString())
                            hash.put("token", loginResult.accessToken.token.toString())
                            hash.put("last_name", jsonObject.get("last_name").toString())
                            hash.put("gender", jsonObject.get("gender").toString())
                            hash.put("birthday", jsonObject.get("birthday").toString())
                            hash.put("register_mode", "facebook")

                            launchRegisterActivity(hash)
                        }
                ).executeAsync()
            }

            override fun onCancel() {
                Log.i("TEST", "log cancel")
            }

            override fun onError(error: FacebookException) {
                Log.i("Login", "Facebook Log fail")
                val toast = Toast.makeText(baseContext, R.string.login_fail_get_email, Toast.LENGTH_LONG)
                toast.show()
            }
        })

        testRegister.callOnClick()

    }

    private fun launchRegisterActivity(hash: HashMap<String, Any>) {
        val intent = RegisterActivity.newIntent(baseContext, hash)
        startActivity(intent)

//        val intent = Intent(this, RegisterActivity::class.java)
//        startActivity(intent)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent) {
        super.onActivityResult(requestCode, resultCode, data)
        twitterLoginButton!!.onActivityResult(requestCode, resultCode, data)
        callbackManager.onActivityResult(requestCode, resultCode, data)

    }

}
