from django.http import HttpResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer

from common.utils import CsrfExemptSessionAuthentication


class JSONResponse(HttpResponse):
    def __init__(self, data=None, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JSONResponse, self).__init__(content, **kwargs)


class LiveeduGenericView(GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer, **kwargs):
        return serializer.save(**kwargs)

    def create_raw(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer, **kwargs)

        return serializer.data

    def create(self, request, *args, **kwargs):
        data = self.create_raw(request, *args, **kwargs)
        return JSONResponse(data)

    def list(self, request, *args, **kwargs):
        data = self.list_raw(request, *args, **kwargs)
        return JSONResponse(data)

    def list_raw(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data
