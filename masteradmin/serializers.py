from rest_framework import serializers
from masteradmin.models import PropertyMaster,PropertyUnits,TenantProfile
from user.serializers import UserSerializer

class PropertySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = PropertyMaster
        fields ='__all__'
        
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)
        try:
            data['units'] = PropertyUnits.objects.filter(property_id=instance.id).values()
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