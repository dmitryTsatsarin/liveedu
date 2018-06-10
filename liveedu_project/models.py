# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Project(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    project = models.ForeignKey(Project, related_name='rating_rel')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, null=True)
    anonymous_ip = models.GenericIPAddressField(null=True, protocol='IPv4', blank=True)

    def __str__(self):
        return "%s -> %s" % (self.project.title, self.rate)

    @staticmethod
    def is_limit_reached(user):
        limit = 15
        limit_is_reached = Rating.objects.filter(user=user).count() >= limit
        return limit_is_reached
