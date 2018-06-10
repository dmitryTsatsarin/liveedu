"""liveedu URL Configuration

"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from liveedu_project import views

urlpatterns = [
    url(r'^add/', views.create_project),
    url(r'^index/', views.show_index_page),
    url(r'^list/', views.GetProjectListView.as_view()),
    url(r'^user/list/', views.GetUserListView.as_view()),
    url(r'^rate/', views.RateTheProjectView.as_view()),

]
