from django.contrib.auth.models import (
    User,
    Group
)
from django.utils import timezone

from rest_framework import serializers

from project_management.models import (
    Project,
    Task
)
from project_management.tasks import send_email_task

from SimpleTaskManager.utils.url_kwargs_consts import (
    PROJECT_URL_KWARG
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
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'performer')

    def validate(self, data):
        if data['due_date'] < timezone.datetime.now().date():
            raise serializers.ValidationError({'due_date': 'due_date shall not be earlier than today.'})
        return data

    def create(self, validated_data):
        validated_data[PROJECT_URL_KWARG] = self.context['view'].kwargs[PROJECT_URL_KWARG]
        task = Task(**{k: v for k, v in validated_data.items() if v})
        task.save()

        mail_body = 'Hello {}!\n You have been appointed to a new task: {}\n Here is description:{}' \
            .format(task.performer.username, task.title, task.description)

        send_email_task.delay("New Task", mail_body, task.performer.email)

        return task


class TaskPerformerSerializer(TaskSerializer):
    performer = ProjectUserSerializer()
