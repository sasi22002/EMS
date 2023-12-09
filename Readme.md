## REAL ESTATE MANAGEMENT | Backend

### Installation 
First ensure you have python globally installed in your computer. If not, you can get python [here](https://python.org).

### Install IDE
Install VisualStudio Code in your computer. Use the [this](https://code.visualstudio.com/download) link to install VisualStudio Code.

### Setup

After doing this, confirm that you have installed virtualenv globally as well. If not, run this:

    $ pip install virtualenv

Then, Git clone this repo to your PC

    $ git clone - git clone **url
    $ cd rems
    
### Create a virtual environment

    $ virtualenv .venv && source .venv/bin/activate
### Install dependancies

    $ pip install -r requirements.txt

### Create a .env file inside uranus_api folder & this file must consist the following keys--
environment="development"

### Place the following file inside configuration folder

    1.development.py
    
<!-- Make migrations & migrate -->

    $ python manage.py makemigrations && python manage.py migrate

<!-- Then we have to add master datas in database  -->
    1.Role
    2.Admin account
    3.Units - 1bhk  #this info is already statically mentioned in enum.py
   
    
<!-- Commands to create above datas: -->
    1.python manage.py create_role  --- NOTE -> roles are mentioned in ENUM file /utils/enum.py
    2.python manage.py create_units


### Launching the app
    $ python manage.py runserver


### Roles
    1 - Admin
    2 - Tenant

## Add below in development file & make sure to change the values regarding with your project
<!-- COPY BELOW THIS IN DEVELOPMENT.PY FILE 

#configuration credentials
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#DATABASE CREDENTIALS

DATABSE_CONFIG={
    'ENGINE': 'django.db.backends.mysql',
    'NAME':'DBNAME',
    'USER' :'USER',
    'PASSWORD' :'PASSWORD',
    'HOST' :'localhost',
    'PORT' :'3306',
}

#EMAIL CREDENTIALS

EMAIL_CONFIG={    
    'EMAIL_BACKEND':'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST' :'smtp.gmail.com',
    'EMAIL_USE_TLS':True,
    'EMAIL_PORT' :587,
    'EMAIL_HOST_USER' :"EMAIL",
    'EMAIL_HOST_PASSWORD':"PASSWORD",
    'DEFAULT_FROM_EMAIL' :"SASIKUMAR",
}

#FORGET-PASSWORD LINK DETAILS

PASSWORD_RESET_URL ="http://127.0.0.1:4200/reset"
PASSWORD_RESET_TIME =300

#TWILIO CREDENTIALS - OTP

TWILO_CONFIG={              
   'TWILIO_ACCOUNT_SID':"",
    'TWILIO_AUTH_TOKEN':"",
    'TWILIO_NUMBER' :+11
}

FIRE_BASE =""
AVATAR_IMAGE =""
SECERET_KEYS ='YOUR SECRETKEY'
   
CONFIG={
    "ALLOWED_HOST":'[*]',
    "LOGO_PATH":"",
    "PYTHON_PATH":"",
    "BASE_PATH":BASE_DIR,
    "LANGUAGE_CODE":"en-us",
    "TIME_ZONE":"UTC",
    "STATIC_URL":"static/",
    "USE_I18N":True,
    "USE_TZ":True,
    "log_path":os.path.join(BASE_DIR, 'Log')
}

IP_CONFIG=['127.0.0.01','132.1.2.2']
ALLOWED_COUNTY=['IN','AUS','US','UK','RSA']

TIME_ZONE ="IND"


#PUSH NOTIFICATION KEYS
FIRE_BASE = ""


#ADMIN DEATILS FOR CREATE A SUPERADMIN

ADMIN_EMAIL =""
ADMIN_USERNAME=""

SERVER_URL="http://127.0.0.1:8000/"

-->
