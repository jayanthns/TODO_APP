import datetime
from rest_framework import serializers

from app.task_app.models import Task
from common.constants import TASK_STATUS


class MessageResponseSerializer(serializers.Serializer):
    """Normal serializer which is used for swagger doc"""
    data = serializers.DictField()
    message = serializers.CharField(max_length=100)
    status = serializers.IntegerField()
    code = serializers.IntegerField()

    class Meta:
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'scheduled_at', 'status')

    def validate_status(self, status):
        if status not in TASK_STATUS:
            raise serializers.ValidationError(F"status must be one of {TASK_STATUS}")
        return status

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        Task.objects.filter(id=instance.id).update(**validated_data)
        return ""


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'scheduled_at', 'status', 'created_at',
                  'modified_at')


class TaskSwaggerSerializer(MessageResponseSerializer):
    data = TaskSerializer()

    class Meta:
        fields = "__all__"


class TaskListSwaggerSerializer(MessageResponseSerializer):
    data = TaskSerializer(many=True)

    class Meta:
        fields = "__all__"
