from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    def create(self,data):
        password = data.pop("password")
        user = User(**data)
        user.set_password(password)
        user.save()
        return user
    
    def validate_email(self,email):
        user = User.objects.filter(email = email)
        if user :
            raise serializers.ValidationError('A user with this e-mail already exists')
        return email
        
    def validate_username(self,username):
        user = User.objects.filter(username = username)
        if user:
            raise serializers.ValidationError('A user with this username already exists')
        else :
            return username

    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','is_staff']



class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','is_staff']

    def update_user(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.is_staff = validated_data.get('is_staff',instance.is_staff)
        instance.save()
        return instance



class UpdateUserProfileSerializer(serializers.ModelSerializer):
    def validate_email(self,email):
        user = User.objects.filter(email = email)
        if user :
            raise serializers.ValidationError('A user with this e-mail already exists')
        return email
        
    def validate_username(self,username):
        user = User.objects.filter(username = username)
        if user:
            raise serializers.ValidationError('A user with this username already exists')
        else :
            return username
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def update_user(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('last_name', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)
