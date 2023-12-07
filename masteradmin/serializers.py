from rest_framework import serializers
from masteradmin.models import PropertyMaster,PropertyUnits

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
        
  