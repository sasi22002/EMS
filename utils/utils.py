from utils.enum import RoleEnum
from django.contrib.auth.hashers import make_password
from user.serializers import UserSerializer
import logging
from user.models import UserRole,User, save_user_role
from utils.helpers import login_details


        

def save_user(request):
    
    #SAVE BOTH USER REGISTERATION HERE
    try:
        if request['role'] == RoleEnum.tenant.value:
            request['password'] = make_password(request['password'])
            user = UserSerializer(data=request)
            user.is_valid(raise_exception=True)
            user.save()
            
            #SAVE RELATED ROLE
            save_user_role(request['role'],user.data['id'])              
            
            user = User.objects.filter(id=user.data['id']).last()           
            return login_details(user,request['role'])
        
        else:
            #CONDITION HAVE TO ADD FOR ANOTHER TYPE USER
            pass
                 
            
    except Exception as e:
        logging.info(f"{e} - save user")
        raise Exception