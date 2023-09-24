# Donation System(For python 3)
OTP Login and Paytm-Payment Gateway On Python-Django

* First clone the project, open your terminal and enter the command

* Now create a virtual environment
```
virtualenv paytm
```
* Now activate the virtual environment
```javascript
source paytm/bin/activate
```
* Now enter into the project folder

* Now go to payments ->settings.py and enter your credentials
```
PAYTM_MERCHANT_KEY=  "<YOUR-PAYTM-MERCHANT-KEY>"
PAYTM_MERCHANT_ID = "<YOUR-PAYTM-MERCHANT-ID>"
PAYTM_CALLBACK_URL = "http://localhost:8000/response/"
```
*Staging Credentials
```
PAYTM_MERCHANT_KEY = "q2Gsj85IICMmmW7U"
PAYTM_MERCHANT_ID = "ALzsRq87951462159458"
PAYTM_WEBSITE = 'WEB_STAGING'
```

*Make Migrations
```
python manage.py makemigrations
```

*Migrate app for transactions details

*Create Super user
```
python manage.py createsuperuser
```

* Now in terminal run the server and go to http://localhost:8000/
```
python manange.py runserver
```
* Install Requirements
*Go to
```
1) http://localhost:8000/web/login/
   - now go to register page if you are new user
2) Register data and login with username and password.
3) Now app with redirect to OTP Verification page with auto fill contact number value
4) Complete OTP Verification.
5) Now it will redirect to your donation member page. 
6) Enter amount you want to Donate and click on Pay Now Button.
7) This should redirect you to Paytm Page.
Test Credentials to use for login:

Mobile Number – 7777777777
Password – Paytm12345

```

### Stuff used to make this:

 * [PAYTM API DOCUMENTATION](http://paywithpaytm.com/developer/paytm_api_doc/) 
 * [SDK DOCUMENTATION](http://paywithpaytm.com/developer/paytm_sdk_doc/) 
