import django_filters
from rest_framework import viewsets, filters

from .models import TestModel
from .serializer import TestModelSerializer


class TestModelViewSet(viewsets.ModelViewSet):  # model vew setを使うとREST一気に定義できる
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
