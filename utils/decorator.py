from rest_framework.exceptions import PermissionDenied
from utils.enum import RoleEnum
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import logging
from django.db.models import Q
from user.models import User
from jwt import decode as jwt_decode
from django.conf import settings
from utils.response_message import Message

def get_user_info(function):
    @wraps(function)
    def wrap(cls, *args, **kwargs):
        try:
            user=User.objects.filter(id=cls.request.user.id).last()
            cls.request.userdata = user
            
            return function(cls, *args, **kwargs)
        except Exception as e:
            logging.info(e,"issue in decorator-get_user_info",exc_info=True)
            res = {'status':False,'message':'Dont have permissions to access this','data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
    return wrap

def super_admin_permission(function):
    @wraps(function)
    def wrap(cls, *args, **kwargs):
        try:
            user=User.objects.filter(id=cls.request.user.id,userrole_user__role=RoleEnum.superadmin.value).prefetch_related('userrole_user').exists()
            if user:            
                return function(cls, *args, **kwargs)
            raise Exception
        except Exception as e:
            logging.info(e,"issue in decorator-superadmin_permission")
            res = {'status':False,'message':'Dont have permissions to access this','data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
    return wrap




def get_user_token(function):
    @wraps(function)
    def wrap(cls, *args, **kwargs):
        try:
           
            req_jwt = cls.request.headers['Authorization'].replace("Bearer ", "")
            decoded_data = jwt_decode(req_jwt, settings.SECRET_KEY, algorithms=["HS256"])

            cls.request.user_info = decoded_data
            return function(cls, *args, **kwargs)
        
        except Exception as e:
            logging.info(e,"issue get_user_token")
            res = {'status':False,'message':Message.server_busy,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
    return wrap


