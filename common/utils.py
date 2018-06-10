from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication


def create_user_and_login(client):
    username = 'dmitry'
    email = 'dmitry.tsatsarin@mailforspam.com'
    password = 'password'
    user = User.objects.create_user(username, email, password)
    client.login(username=username, password=password)
    return user


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return
