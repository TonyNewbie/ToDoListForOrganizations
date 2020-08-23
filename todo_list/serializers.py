from .models import Task, CustomUser
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'owner', 'creation_date', 'status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'organizations',)
