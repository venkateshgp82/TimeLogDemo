from rest_framework import serializers
from .models import Project, Timelog, UserProfile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "project_id"]

    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=500)
    project_id = serializers.CharField(max_length=25)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.save()
        return instance
    
class TimelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timelog
        fields = ["work_hours", "project", "user", "date"]
    
    def create(self, validated_data):
        return Timelog.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.work_hours = validated_data.get("work_hours", instance.work_hours)
        instance.project = validated_data.get("project", instance.project)
        instance.user = validated_data.get("user", instance.user)
        instance.date = validated_data.get("date", instance.date)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'project']

