import json

from rest_framework.test import APITestCase, APIClient

from common.utils import create_user_and_login


class CommonTestCaseMixin(object):
    user = None

    def login_as(self):
        self.user = create_user_and_login(self.client)
        return self.user

    def content_to_dict(self, content):
        return json.loads(content)


class LiveeduTestCase(APITestCase, CommonTestCaseMixin):
    client_class = APIClient
