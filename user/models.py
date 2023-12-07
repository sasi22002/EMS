from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager
)

from utils.enum import GenderEnum
from django.db import transaction
from utils.enum import RoleEnum
import logging



def save_user_role(role,user):
    try:
        user = UserRole.objects.update_or_create(role_id=role,user_id=user)
        return user
    except Exception as e:
        logging.info(f"{e}: save_user_role")
        raise Exception
    
    
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                
                #SAVE RELATED ROLE
                save_user_role(RoleEnum.superadmin.value,user.id)     
                return user
        except:
            raise Exception('Model creation Error')

    

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class Role(models.Model):
    """
    User roles
    1 - ADMIN
    2 - USER

    Args:
        models (_type_):user roles
    """
    role_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default= True)
    class Meta:
        db_table = 'role_master'
        

# User related tables
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=126, unique=True,null = False)
    username = models.CharField(max_length =60)
    password = models.CharField(max_length=256,null = True,blank = True)
    phone_number=models.CharField(max_length=128,null=True,unique=True)
    address = models.CharField(max_length=256,null = True)
    date_of_birth = models.CharField(max_length=16,blank=True,null=True)
    gender = models.CharField(max_length=8,default=GenderEnum.Not_to_say.value,blank=True,null=True)
    profile_picture = models.TextField(null=True,blank=True)
    is_block = models.BooleanField(default= False)
    is_staff =  models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)   
    last_login = models.DateTimeField(blank=True,null=True)
    

    class Meta:
        db_table = 'auth_master'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
   


class UserRole(models.Model):
    """
    Args:
        models : Model for mapping user with respective roles
    """
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='user_role',null = True,blank=True)
    user=models.ForeignKey(User,related_name='userrole_user',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default= True)
    
    class Meta:
        db_table = 'user_roles'
        
        

class UserActivityLog(models.Model):
    """
    Args:
        models: Model for save the User activity details with API payload data
    """
    user=models.ForeignKey(User,related_name='user_activity',null=True,on_delete=models.CASCADE)
    activity_details = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)
              
    class Meta:
        db_table = 'activity_log'


class UserSession(models.Model):
    """
    Args:
        models : Model for save the User Sessions with Access/Refresh tokens
    """
    access_token = models.TextField()
    refresh_token = models.TextField(null=True)
    auth=models.ForeignKey(User,related_name='auth_session',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    sessiontext = models.TextField(max_length=220)
    loggedin_as = models.IntegerField(null=True)


    class Meta:
        db_table = 'user_session'
        
        
