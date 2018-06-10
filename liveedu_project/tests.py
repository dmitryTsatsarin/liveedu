# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status as rest_status

from common.testing import LiveeduTestCase
from liveedu_project.factories import ProjectFactory, UserFactory, RatingFactory
from liveedu_project.models import Rating, Project


class GetListProjectTestCase(LiveeduTestCase):

    def tearDown(self):
        Project.objects.all().delete()

    def test_get_list(self):
        user = self.login_as()

        ProjectFactory.create(title='title1', description='description1', user=user)
        ProjectFactory.create(title='title2', description='description2', user=user)
        response = self.client.get('/project/list/')
        content_dict = self.content_to_dict(response.content)
        self.assertEquals(len(content_dict), 2)

    def test_get_list_with_rate(self):
        user = self.login_as()
        project = ProjectFactory.create(title='title1', description='description1', user=user)
        RatingFactory.create(rate=3, project=project, user=user)
        response = self.client.get('/project/list/')
        print Project.objects.count()
        content_dict = self.content_to_dict(response.content)
        print content_dict
        self.assertEquals(len(content_dict), 1)
        self.assertEquals(content_dict[0]['rate'], 3)


class GetUserListTestCase(LiveeduTestCase):

    def test_get_user_list(self):
        user = self.login_as()

        UserFactory.create(username='username1')
        UserFactory.create(username='username2')
        response = self.client.get('/project/user/list/')
        content_dict = self.content_to_dict(response.content)

        self.assertEquals(len(content_dict), 3)


class RateTheProjectTestCase(LiveeduTestCase):

    def test_ok(self):
        user = self.login_as()
        project = ProjectFactory.create(title='title1', description='description1', user=user)
        data_in = {
            'project_id': project.id,
            'rate': 4
        }
        response = self.client.post('/project/rate/', data=data_in, format='json')
        self.assertEquals(Rating.objects.count(), 1)
        self.assertEquals(Rating.objects.get().rate, 4)

    def test_limit(self):
        user = self.login_as()
        project = ProjectFactory.create(title='title1', description='description1', user=user)
        RatingFactory.create_batch(15, rate=5, project=project, user=user)
        data_in = {
            'project_id': project.id,
            'rate': 4
        }
        response = self.client.post('/project/rate/', data=data_in, format='json')
        self.assertEquals(response.status_code, rest_status.HTTP_400_BAD_REQUEST)
        content_dict = self.content_to_dict(response.content)
        self.assertTrue('message' in content_dict.keys())

    def test_anonymous(self):
        user = UserFactory.create(username='username1')
        project = ProjectFactory.create(title='title1', description='description1', user=user)
        data_in = {
            'project_id': project.id,
            'rate': 5
        }
        response = self.client.post('/project/rate/', data=data_in, format='json')
        self.assertEquals(Rating.objects.count(), 1)
        self.assertEquals(Rating.objects.get().rate, 5)

    def test_error_on_duplicate_for_anonymous(self):
        user = UserFactory.create(username='username1')
        project = ProjectFactory.create(title='title1', description='description1', user=user)
        RatingFactory.create(rate=1, project=project, anonymous_ip='127.0.0.1')
        data_in = {
            'project_id': project.id,
            'rate': 5
        }
        response = self.client.post('/project/rate/', data=data_in, format='json')
        print response.content
        self.assertEquals(response.status_code, rest_status.HTTP_400_BAD_REQUEST)
        content_dict = self.content_to_dict(response.content)
        self.assertTrue('message' in content_dict.keys())
