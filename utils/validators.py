import logging,copy
from utils.enum import RoleEnum


def signup_validator(data):
    try:
        if data['role'] == RoleEnum.tenant.value:
            json_keys=['username' ,'role',"email","phone_number","password","confirm_password"]
                   
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    
    except Exception as e:
        logging.info(e)
        return False
    

def socialsignup_validator(data):
    try:
        if data['role'] == RoleEnum.tenant.value:
            json_keys=['username' ,'role',"email","phone_number","social_id","social_type"]
          
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    
    except Exception as e:
        logging.info(e)
        return False

def null_key_validator(request):
    try:
        data=copy.deepcopy(request.data)
    
        for val in data:
            if len(str(request.data[val])) == 0 or request.data[val] == None:
                return False
        return True
    except Exception as e:
        logging.info(e)
        return False

