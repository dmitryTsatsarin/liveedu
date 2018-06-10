from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from liveedu_project.models import Project, Rating


class GetProjectListSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True, source='user.username')
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['user', 'title', 'description', 'rate', 'id']

    def get_rate(self, project):
        user = self.context['request'].user
        if user.is_authenticated:
            if Rating.objects.filter(user=user, project_id=project.id).exists():
                return Rating.objects.filter(user=user, project_id=project.id).get().rate
            else:
                return 0
        else:
            ip = self.context['request'].META.get('REMOTE_ADDR')
            if Rating.objects.filter(anonymous_ip=ip, project_id=project.id).exists():
                return Rating.objects.filter(anonymous_ip=ip, project_id=project.id).get().rate
            else:
                return 0


class GetUserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RateTheProjectSerializer(Serializer):
    project_id = serializers.IntegerField()
    rate = serializers.IntegerField(min_value=1, max_value=5)
