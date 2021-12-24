import django_filters
from rest_framework import viewsets, filters

from .models import Stage
from .serializer import StageSerializer


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
