from rest_framework import permissions,status
import logging
from utils.pagination import pagination_class,pagination_func
from utils.enum import RoleEnum
from utils.validators import *
from django.contrib.auth import authenticate
from django.db import transaction
from utils.response_message import Message
from utils.decorator import *
from rest_framework.views import APIView
from utils.helpers import login_details
from utils.utils import save_user
from user.models import UserSession
from utils.swagger_doc import login,signup
from django.views.decorators.csrf import csrf_exempt
import requests



# your_app/views.py

from django.shortcuts import render

@csrf_exempt
def login_page(request):
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def manage_property(request):
            
    return render(request, 'manage_property.html')

class SignUp(APIView):
    permission_classes=[permissions.AllowAny]
    
    @transaction.atomic()
    @signup #SWAGGER DOCS
    def post(self,request):
        try:
            data=request.data

            #BASIC VALIDATIONS
            validate = signup_validator(data)
            if not validate:
                res={'status':False,'message':Message.data_missing,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            #NONE TYPE VALIDATIONS
            validate_null = null_key_validator(request)
            if not validate_null:
                res={'status':False,'message':Message.mandatory_keys,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            #EMAIL AND PHONE NUMBER VALIDATIONS
                                    
            check_phone = User.objects.filter(phone_number=data['phone_number'],is_active=True).exists()
            check_email = User.objects.filter(email=data['email'],is_active=True).exists()
            
            if check_phone :
                res={'status':False,'message':Message.phonenumber_exist,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST) 
            if check_email:
                res={'status':False,'message':Message.email_exist,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST) 
                
            #PASSWORD AND CONFIRM PASSWORD VALIDATIONS
            
            if data['password'] != data['confirm_password']:
                res={'status':False,'message':Message.password_mismatched,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)  
                        
            #SIGNUP A NEW USER           
            user_data = save_user(data)            
                                                          
            res = {'status':True,'message':Message.signup,'data':[user_data]}
            return Response(res,status=status.HTTP_200_OK)
          
        except Exception as e:
            transaction.set_rollback(True)
            logging.info(f"{e}: signup screen",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    """
    Login for All users    
    """
    permission_classes = [permissions.AllowAny]
        
    @csrf_exempt
    @login #SWAGGER DOCS
    def post(self,request):
        try:
            email= request.data['email']          
            password = request.data['password']
            role = request.data['role']
            
            #VALIDATING THE REQUESTED PAYLOAD
            if email == None:
                res = {'status':False,'message':Message.enter_email,'data':[],'screen_staus':None}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            if password == None:
                res = {'status':False,'message':Message.enter_password,'data':[],'screen_staus':None}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            email = User.objects.filter(email=email,userrole_user__role_id=role,is_active=True).prefetch_related('userrole_user').last() 
            if role==RoleEnum.superadmin.value:
                email = User.objects.filter(email=request.data['email'],is_active=True).last() 
                
            if not email:
                res = {'status':False,'message':Message.register_mail,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            #AUTH FUNCTION TO LOGIN
            if role == RoleEnum.superadmin.value:
                user = authenticate(request, email=email.email, password=password)
            if role == RoleEnum.tenant.value:           
                user = authenticate(request, email=email.email, password=password)
                                            
            if user is None:
                res = {'status':False,'message':Message.invalid_password,'data':[]}
                return Response(res,status = status.HTTP_400_BAD_REQUEST) 
            
            if user.is_block:
                res = {'status':False,'message':Message.login_block,'data':[],'screen_staus':None}
                return Response(res,status = status.HTTP_400_BAD_REQUEST)
            
            #GENERATE ACCESS & REFRESH TOKENS 
            user_data = login_details(user,role)
            res = {'status':True,'message':Message.login_success,'data':[user_data]}
            return Response(res,status=status.HTTP_200_OK)
                          
        except Exception as e:
            logging.info(f"{e}: Login",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

        
    def post(self,request):
        try:
            user = request.user.id

            UserSession.objects.filter(auth_id=user).update(is_active=False)
            
            res = {'status':True,'message':Message.logout_success,'data':[]}
            return Response(res,status=status.HTTP_200_OK)
            
        except Exception as e:
            logging.info(f"{e}: Logout",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        