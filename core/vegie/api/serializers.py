from rest_framework import serializers
from ..models import Receipe
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Users = ReceipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ReceipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Receipe
        fields = "__all__"
        depth = 1


