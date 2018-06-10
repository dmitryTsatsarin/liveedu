"""liveedu URL Configuration

"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from liveedu_project.views import show_index_page

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^accounts/', include('registration.backends.simple.urls')),
                  url(r'^project/', include('liveedu_project.urls')),
                  url(r'^auth/', include('django.contrib.auth.urls')),
                  url(r'^$', show_index_page),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
