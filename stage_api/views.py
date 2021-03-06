import django_filters
from rest_framework import viewsets, filters

from .models import Stage
from .serializer import StageSerializer
from .filter import StageFilter
from .permission import IsStuffOrReadOnlyPermission


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_class = StageFilter
    permission_classes = (IsStuffOrReadOnlyPermission,)
