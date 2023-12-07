from rest_framework import permissions,status
import logging
from utils.validators import *
from django.db import transaction
from utils.response_message import Message
from utils.decorator import *
from rest_framework.views import APIView
from masteradmin.models import  UnitMaster,PropertyMaster

class ManageUnits(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        try:
            data = UnitMaster.objects.filter(is_active=True).values()
            
            res = {'status':True,'message':Message.unit_listed,'data':[]}
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
            exist = PropertyMaster.objects.filter()
            
            
            #CREATE A NEW PROPERTY

            
            res = {'status':True,'message':Message.property_created,'data':[]}
            return Response(res,status=status.HTTP_200_OK)
          
        except Exception as e:
            transaction.set_rollback(True)
            logging.info(f"{e}: signup screen",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)


