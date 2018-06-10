import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from liveedu_project.models import Project, Rating


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username{0}@espresa.com'.format(n))
    email = factory.LazyAttribute(lambda obj: obj.username)
    password = factory.LazyAttribute(lambda obj: make_password(obj.username.split('@')[0]))


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating
