# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from rest_framework.exceptions import ValidationError

from common.views import LiveeduGenericView
from liveedu_project.forms import ProjectForm
from liveedu_project.models import Project, Rating
from liveedu_project.serializers import GetProjectListSerializer, GetUserListSerializer, RateTheProjectSerializer


@login_required(login_url='/auth/login/')
def create_project(request):
    is_saved = False
    if request.method == 'POST':
        form = ProjectForm(request.POST, )
        if form.is_valid():
            form.instance.user = request.user
            form.save()

        is_saved = True
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'is_saved': is_saved,
    }

    return render_to_response('project/add.html', context)


def show_index_page(request):
    return render_to_response('project/index.html')


class GetProjectListView(LiveeduGenericView):
    serializer_class = GetProjectListSerializer

    def get_queryset(self):
        return Project.objects.filter().order_by('rating_rel__rate')

    @method_decorator(cache_page(0))  # 0 seconds, test cache. You can increase if you want long period
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetUserListView(LiveeduGenericView):
    serializer_class = GetUserListSerializer

    def get_queryset(self):
        return User.objects.all()

    @method_decorator(cache_page(0))  # 0 seconds, test cache. You can increase if you want long period
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RateTheProjectView(LiveeduGenericView):
    serializer_class = RateTheProjectSerializer

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer, **kwargs):
        validated_data = serializer.validated_data
        user = self.request.user
        if user.is_authenticated:
            if Rating.objects.filter(user=user, project_id=validated_data['project_id']).exists():
                raise ValidationError({'message': 'You are rated this project already'})

            if Rating.is_limit_reached(user):
                raise ValidationError({'message': 'Limit(15) is reached already '})

            return Rating.objects.create(user=user, **validated_data)
        else:
            ip = self.request.META.get('REMOTE_ADDR')
            if Rating.objects.filter(anonymous_ip=ip).exists():
                raise ValidationError({'message': 'You are not registered user. You can rate only one project'})
            return Rating.objects.create(anonymous_ip=ip, **validated_data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
