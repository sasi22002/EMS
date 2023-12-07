from datetime import datetime,timedelta
import random,logging,string,random
from django.core.mail import EmailMessage
from utils.enum import RoleEnum
from utils.enum import StaticEnum
from user.models import User,UserRole,UserSession
from masteradmin.models import PropertyMaster
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import json,logging,traceback,sys
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rems.development import TIME_ZONE


def generate_otp():
    # Define possible characters for OTP
    digits = "123456789"
    otp = ""
    # Loop to generate 6 random digits
    for i in range(4):
        otp += random.choice(digits)
    # Return the OTP
    return otp   

def send_mail_woTemplate(subject,mail_body,to_mail,from_mail,**template_data):
    try:
        
        if template_data:
            content = template_data['content']
            template = template_data['template']
            html_content = render_to_string(template, content)
            email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            
        email = EmailMessage(
            subject=subject,body=mail_body,to=[to_mail],from_email=from_mail
        )
        email.send()
        return True
    except Exception as ex:
        raise ex
    
    

class Convertion:
    
    def getIST():
        return datetime.utcnow()+timedelta(hours=5,minutes=30)
    
    def getindian_time(data):        
        val=data + timedelta(hours=5,minutes=30)
        return val
    
    def convert_UTC(data):                
        if TIME_ZONE == StaticEnum.IND.value:
            val=data + timedelta(hours=5,minutes=30)
        else:
            val=data - timedelta(hours=7)
            
        return val
    
    def getGREECE():
        return datetime.utcnow()+timedelta(hours=2)
    
    def getgreece_time(data):        
        val=data + timedelta(hours=2)
        return val
    
    def getUTC():
        return datetime.utcnow()
            
    def convert_str_time(time):
        try:
            _sttime=time.strftime('%d %B %Y %I.%M %p')
            return _sttime
        except:
            logging.warning('error while converting')
            return time
        
        
    def convert_strptime_timezone(time):
        try:
            try:
                _sttime=datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%fz')
                return _sttime
            except:
                _sttime=datetime.strptime(time,'%Y-%m-%dT%H:%M:%Sz')
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time
    
    
    def convert_strptime(time):
        try:
            try:
                _sttime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S.%f')
                return _sttime
            except:
                _sttime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time

    def convert_strptime_format(time,format):
        try:
            try:
                _sttime=datetime.strptime(time,format)
                return _sttime
            except:
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time
    
    
        

        
def generate_randpassword(userid):
    try:
        import secrets
        from django.contrib.auth.hashers import make_password

        password_length = 6
        rand_passowrd = secrets.token_urlsafe(password_length)
        hash_passowrd = make_password(rand_passowrd)
        
        save_temppassword = User.objects.filter(id=userid).update(password=hash_passowrd)
        return rand_passowrd
        
    except Exception as e:
        raise Exception
        

def split_pagedatas(page,item):
    page = int(page)
    item = int(item)
    start = item *(page-1)
    end = item * page
    return [start,end]
 

class LogInfo:
    def __init__(self,error):
        logging.info(error)
        logging.error(traceback.format_exception(*sys.exc_info()))
        pass

    def return_response(error,message):
        logging.info(error)
        logging.error(traceback.format_exception(*sys.exc_info()))
        res = {'status':False,'message':message,'data':[]}
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
    
        
        

def auth_token(user,role):
    #FUNCTION FOR CREATE ACCESS & REFRESH TOKENS FOR USER
    
    emp_id=User.objects.get(email=user.email).id
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.email
    access['user_id']=emp_id
    access['role']=role
    refresh['email']=user.email
    refresh['user_id']=emp_id
    refresh['role']=role
    
    #sAVE LAST LOGIN TIME
    login_time = User.objects.filter(id=emp_id).update(last_login=datetime.now())
    
    #SAVE USER SESSION DETAILS
    save_user_sessionsdata(access,refresh,emp_id,role)
      
    return {"access_token": str(access),
    "refresh_token":str(refresh)}
    

def get_user_role(user):
    try:
        user_role = UserRole.objects.filter(user_id=user).last()
        return user_role.role.id
    except Exception as e:
        logging.info(f"{e}: get_user_role function")
        raise Exception
    

def login_details(user,role):
    #FUNCTION TO ARRANGE THE USER LOGIN DETAILS
    
    try:
        user_details = {}
        get_jwt = auth_token(user,role)
        user_details['access_token'] = get_jwt['access_token']
        user_details['refresh_token'] = get_jwt['refresh_token']
        user_details['role'] = role
        user_details['email'] = user.email
        user_details['user_id'] = user.id
        user_details['user_name'] = user.username
        user_details['profile_pic'] = user.profile_picture
        if get_user_role(user)==RoleEnum.superadmin.value:
            user_details['is_superuser']=True
        else:
            user_details['is_superuser']=False        
        return user_details
        
    except Exception as e:
        logging.info(f"{e}: login details func")
        raise Exception
        

def generate_sessionskeys():
    count =1
    while count < 10:
        length = 4
        possible_numbers = "1234567890"
        random_nummber_list = [random.choice(possible_numbers) for i in range(length)]
        random_num = "".join(random_nummber_list)
        char_length = 15
        possible_numbers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_nummber_list = [random.choice(possible_numbers) for i in range(char_length)]
        random_name = "".join(random_nummber_list)
        res = random_name +random_num
        check = UserSession.objects.filter(sessiontext=res).exists()
        if not check:
            break
        count += 1
    return res


def save_user_sessionsdata(access,refresh,empid,role):
    try:
       sessionkey = generate_sessionskeys()
       data = UserSession.objects.filter(auth_id=empid).exists()
       if data:
           update_ = UserSession.objects.filter(auth_id=empid).update(access_token=access,refresh_token=refresh,sessiontext=sessionkey,loggedin_as=role)
       else:
           create_ = UserSession.objects.create(auth_id=empid,access_token=access,refresh_token=refresh,sessiontext=sessionkey,loggedin_as=role)
    except Exception as e:
       logging.info(e,'sessions not saved')
       pass

def generate_password():
    letters= string.ascii_letters
    digits= string.digits
    alphabet= letters+ digits
    password=''
    for i in range(8):
        password+= ''.join(random.choice(alphabet))
    return password



def generate_uniqueids():
    try:
        prop_id = PropertyMaster.objects.filter(property_code__isnull=False).last()        
        count = 1
        while count < 10:
            prop_id = prop_id.property_code[5:]
            prop_id = int(prop_id) + count
            prop_id = '{:01}'.format(prop_id)
            prop_id = "REMS_" + str(prop_id)
            count += 1
            if PropertyMaster.objects.filter(property_code=prop_id).count() == 0:
                break
        return prop_id
    
    except Exception as e:
        prop_id = "REMS_" + "1"
        return prop_id
    
def has_duplicates(data,val):
    seen_ids = set()
    for entry in data:
        unit_id = entry.get(val)
        if unit_id in seen_ids:
            return True  # Duplicate found
        seen_ids.add(unit_id)
    return False  # No duplicates found