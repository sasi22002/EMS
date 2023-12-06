from rest_framework import serializers
import json,logging
from user.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        extra_kwargs = {'password': {'write_only': True},'social_id': {'write_only': True},'social_type': {'write_only': True}}
        # fields ='__all__'
        
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.Meta.exclude = ['user_permissions','groups','updated_at','is_superuser']
        
  