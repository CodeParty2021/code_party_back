import django_filters
from rest_framework import viewsets, filters

from .models import Step
from .serializer import StepSerializer
from .filter import StepFilter
from .permission import IsStuffOrReadOnlyPermission


class StepViewSet(viewsets.ModelViewSet):
    """
    ここに説明をかける。
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    filter_class = StepFilter
    permission_classes = (IsStuffOrReadOnlyPermission,)
