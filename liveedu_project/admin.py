# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from liveedu_project.models import Project, Rating


class ProjectAdmin(ModelAdmin):
    pass


class RatingAdmin(ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Rating, RatingAdmin)
