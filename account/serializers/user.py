from django.conf import settings
from rest_framework import serializers
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ("email","password","password2")
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password2(self, value):
        password1 = self.get_initial().get('password')
        
        if password1 and password1 != value:
            raise serializers.ValidationError("Passwords mismatched")
        
        return value
    
    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        
        user.set_password(validated_data.get('password'))
        user.save()

        return user




