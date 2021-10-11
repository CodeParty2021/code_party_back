

# Create your views here.
import django_filters
from rest_framework import viewsets, filters

from .models import TestModel
from .serializer import TestModelSerializer


class TestModelViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
