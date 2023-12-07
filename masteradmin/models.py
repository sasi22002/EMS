from django.db import models
from user.models import User




class PropertyMaster(models.Model):
    """
    Args:
        models : Model for save the Property Details
    """
    
    property_name = models.TextField(null=False)
    property_code = models.CharField(null=False,max_length=25)
    ul_pin = models.CharField(null=False,max_length=20)
    pincode = models.BigIntegerField(null=False)
    address = models.TextField(null=False)
    lattitude = models.CharField(max_length=96,null=True)
    longtitude = models.CharField(max_length=96,null=True)
    features = models.JSONField(null=True)
    auth=models.ForeignKey(User,related_name='user_property',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        db_table = 'property_master'
        


class UnitMaster(models.Model):
    """
    Args:
        models : Model for save the Property Unit master like 1BHK,2BHK....
    """
    
    unit_name = models.CharField(max_length=30,null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        db_table = 'unit_master'
           

class PropertyUnits(models.Model):
    """
    Args:
        models : Model for save the Property with relative Units
    """
    property=models.ForeignKey(PropertyMaster,related_name='propertyunit',null=False,on_delete=models.CASCADE)
    unit=models.ForeignKey(UnitMaster,related_name='propertyunit_unit',null=False,on_delete=models.CASCADE) 
    base_rent = models.FloatField(default=0)
    cost =   models.FloatField(default=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        db_table = 'property_units'
        

class TenantProfile(models.Model):
    """
    Args:
        models : Model for save the Tenant Informations
    """
    user=models.ForeignKey(User,related_name='tenant_user',null=False,on_delete=models.CASCADE)
    document = models.JSONField(null=False)
    is_docs_verified = models.BooleanField(default=True)
    occupation = models.CharField(max_length=30)
    is_salaried = models.BooleanField(default=False)
    own_business = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        db_table = 'tenant_profile'
        
        

class TenantProperty(models.Model):
    """
    Args:
        models : Model for save the Tenant Informations
    """
    tenant=models.ForeignKey(TenantProfile,related_name='tenant_profile',null=False,on_delete=models.CASCADE)
    aggrement_date = models.DateTimeField(null=False)
    duration_days = models.IntegerField(default=0)
    aggrement_enddate = models.DateTimeField(null=False)
    monthly_rent = models.FloatField(null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        db_table = 'tenant_property'
        
        
