import logging,json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user.models import User,UserActivityLog,UserSession
from utils.helpers import Convertion
from django.utils import timezone
from utils.enum import RoleEnum


class LoginRequiredMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # response = get_response(request)       
    
    def __call__(self, request):
        response = self.get_response(request)
        try:
            """CHECK THE REQUESTED USER IS BLOCKED OR NOT IN  AUTH-USER TABEL"""
            BLOCK_USER = User.objects.filter(id=request.user.id,is_block=True,is_deleted=True).exists()
            
            DELETED_USER = User.objects.filter(id=request.user.id,is_deleted=True).exists()
            
            if BLOCK_USER:
                """return ERROR message with code 401--------"""
                return JsonResponse({'status':False,'message':'User is Blocked by Admin','data':[]}, status=401)
            
            if DELETED_USER:
                return JsonResponse({'status':False,'message':'Your account is deleted by admin','data':[]}, status=401)
            
            """make a entry in last login in user tabels"""                
            get = User.objects.filter(id=request.user.id).last().last_login

            if get != Convertion.getIST().date():
                login_time = User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                          
        except Exception as e:
            logging.warning('error in middleware',e)
            pass
        
        return response
    



class ActivityLogMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # response = get_response(request)       
    
    def __call__(self, request):
        request_body = request.body
        response = self.get_response(request)
        try:
        
            """CHECK THE REQUESTED USER HAVE ACTIVE SESSION"""

            logger = logging.getLogger('api_access')
            logger.info(f'{request.user.username} accessed {request.path} with {request.method}')
            info = {
                "user":request.user.id,
                "method":request.method,
                "url":request.path,
                "status":response.status_code,
                "request_body":json.dumps(request_body.decode("utf-8")) if request_body else json.dumps({}),
                "response":response.data,
                "browser":request.user_agent.browser
                            
            }            
            logger.info(info)
            
            UserActivityLog.objects.create(user_id=request.user.id if request.user.id else None,activity_details=json.dumps(info))
          
            return response
                               
        except Exception as e:
            logging.warning('error in actvitylog middleware',e)
            pass
        
        return response
    


class CustomSessionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # response = get_response(request)       
    
    def __call__(self, request):
        response = self.get_response(request)
        try:
        
            """CHECK THE REQUESTED USER HAVE ACTIVE SESSION"""
            USER_SESSION = UserSession.objects.filter(auth_id=request.user.id).exists()
                        
            if USER_SESSION:
                """GET THE USER SESSION OBJECTS"""
                get_role = User.objects.filter(id=request.user.id).prefetch_related('userrole_user').last()
                DATA = UserSession.objects.filter(auth_id=request.user.id).last()
                req_jwt = request.headers['Authorization'].replace("Bearer ", "")
                
                
                if str(DATA.access_token) == str(req_jwt):
                    return response
                else:
                    return JsonResponse({'status':False,'message':'Logging Out','data':[]}, status=401)

                
        except Exception as e:
            logging.warning('error in session middleware',e)
            pass
        
        return response