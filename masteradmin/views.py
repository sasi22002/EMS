from rest_framework import permissions,status
import logging
from utils.validators import *
from django.db import transaction
from utils.response_message import Message
from utils.decorator import *
from rest_framework.views import APIView
from masteradmin.models import  UnitMaster,PropertyMaster,PropertyUnits,TenantProfile
from .serializers import PropertySerializer,TenantProfileSerializer
from utils.helpers import generate_uniqueids,has_duplicates
from utils.utils import save_user
from utils.pagination import pagination_class
class ManageUnits(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        try:
            data = UnitMaster.objects.filter(is_active=True).values()
            
            res = {'status':True,'message':Message.unit_listed,'data':data}
            return Response(res,status=status.HTTP_200_OK)
          
        except Exception as e:
            logging.info(f"{e}: ManageUnits",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)


class ManageProperty(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    @transaction.atomic()
    def post(self,request):
        try:
            data=request.data
            
            #EXISTING PROPERTY VALIDATIONS
            exist = PropertyMaster.objects.filter(ul_pin=data['ul_pin'],pincode=data['pincode']).exists()
            if exist:
                res = {'status':False,'message':Message.property_exist,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
                                    
            #CREATE A NEW PROPERTY
            user = User.objects.filter(userrole_user__role_id=RoleEnum.superadmin.value).prefetch_related('userrole_user').last().id
            data['auth'] = user
            data['property_code'] = generate_uniqueids()
            property_data = PropertySerializer(data=data)
            if property_data.is_valid(raise_exception=True):
               
                if len(data['units'])!=0:
                    #CHECK DUPLICATE UNITS
                    if has_duplicates(data['units'],"unit_id"):
                        res = {'status':False,'message':Message.property_unit_exist,'data':[]}
                        return Response(res,status=status.HTTP_400_BAD_REQUEST)
                    else:
                        pass
                    
                    property_data.save()  
                    #SAVE UNITS FOR PROPERTY                         
                    [PropertyUnits.objects.create(property_id=property_data.data['id'],unit_id=val['unit_id'],base_rent=val['base_rent'],cost=val['cost']) for val in data['units']]           
                else:
                    property_data.save()                 
                        
                res = {'status':True,'message':Message.property_created,'data':[]}
            else:
                res = {'status':True,'message':Message.check_property,'data':[]}
                
            return Response(res,status=status.HTTP_200_OK)
          
        except Exception as e:
            transaction.set_rollback(True)
            logging.info(f"{e}: ManageProperty - post",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
    @super_admin_permission
    def get(self,request):
        try:
            #API TO LIST THE ALL PROPERTY DETAILS
            property = PropertyMaster.objects.filter(is_active=True).order_by('-id')
                    
            pagination_result = pagination_class(self,queryset=property,request=request)
            propert_data = PropertySerializer(pagination_result['data'],many=True).data
                  
            res = {'status':True,'message':Message.property_listed_successfuly,'data':propert_data,'total_page':pagination_result['total_pages'], 'total_count':pagination_result['total_count']}
            return Response(res,status=status.HTTP_200_OK)          
            
        except Exception as e:
            logging.info(f"{e}: ManageProperty - post",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)


class ManageTenants(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @super_admin_permission
    def get(self,request):
        try:
            tenant = TenantProfile.objects.filter(is_active=True).order_by('-id')         
            pagination_result = pagination_class(self,queryset=tenant,request=request)
            tenant_data = TenantProfileSerializer(pagination_result['data'],many=True).data
                              
            res = {'status':True,'message':Message.property_listed_successfuly,'data':tenant_data,'total_page':pagination_result['total_pages'], 'total_count':pagination_result['total_count']}
            return Response(res,status=status.HTTP_200_OK)          
            
        except Exception as e:
            logging.info(f"{e}: ManageTenants - get",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
    @super_admin_permission
    def post(self,request):
        try:
            #API FOR CREATE A NEW TENANT
            data = request.data
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
                                          
            res = {'status':True,'message':Message.tenant_created,'data':[]}
            return Response(res,status=status.HTTP_200_OK)          
            
        except Exception as e:
            logging.info(f"{e}: ManageTenants - get",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)