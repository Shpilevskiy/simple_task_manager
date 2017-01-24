from django.contrib.auth.models import (
    User,
    Group
)

from rest_framework import serializers


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#     fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'groups', 'last_name')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def validate(self, data):
        if not data['groups']:
            raise serializers.ValidationError({'groups': 'Group is required.'})
        if Group.objects.get(name='Developers') in data['groups']\
                and Group.objects.get(name='Managers') in data['groups']:
            raise serializers.ValidationError({'error': 'User cannot be developer and manager at same time.'})
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        user.groups.set(validated_data['groups'])
        return user
