from rest_framework import serializers
from masteradmin.models import PropertyMaster,PropertyUnits,TenantProfile,TenantProperty
from user.serializers import UserSerializer


        
class PropertyUnitSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = PropertyUnits
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            tenant = TenantProperty.objects.filter(property_id=instance.id).last()
            data['tenant_info'] = TenantProfile.objects.filter(id=tenant.tenant.id).values() if tenant else []
            
        except:
            data['tenant_info'] =  []
            
        return data
    
    
class PropertySerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = PropertyMaster
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            data['units'] = PropertyUnitSerializer(PropertyUnits.objects.filter(property_id=instance.id),many=True).data
        except:
            data['units'] =  []
            
        return data
  

class TenantProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = TenantProfile
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            data['user_data'] = UserSerializer(instance.user).data
        except:
            data['user_data'] =  []
            
        return data
    

class TenantPropertySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = TenantProperty
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            data['property_detail'] = PropertyMaster.objects.filter(id=instance.property.property.id).values()
            data['unit'] = instance.property.unit.unit_name
        except:
            data['property_detail']= []
            data['unit']  = []
        return data
    

class TenantDetailSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = TenantProfile
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            data['user_data'] = UserSerializer(instance.user).data
            data['properties'] = TenantPropertySerializer(TenantProperty.objects.filter(tenant_id=instance.id),many=True).data
        except:
            data['user_data'] =  []
            data['properties'] = []
            
        return data