from django.contrib.auth.models import (
    User,
    Group
)

from rest_framework import serializers

from project_management.models import (
    Project,
    Task
)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'groups', 'last_name')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def validate(self, data):
        if not data['groups']:
            raise serializers.ValidationError({'groups': 'Group is required.'})
        if Group.objects.get(name='Developers') in data['groups'] \
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


class UserUpdateSerializer(UserSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        if 'groups' in validated_data:
            instance.groups.set(validated_data['groups'])
        instance.save()

        return instance


class ProjectUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'groups')


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=250)
    description = serializers.CharField(max_length=5000, required=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'members', 'description')


class ProjectMembersSerializer(ProjectSerializer):
    members = ProjectUserSerializer(many=True)
