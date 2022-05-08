import django_filters
from rest_framework import viewsets, filters

from .models import Step, StepCode
from .serializer import StepCodeSerializer, StepSerializer
from .filter import StepCodeFilter, StepFilter
from .permission import IsStuffOrReadOnlyPermission


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    filter_class = StepFilter
    permission_classes = (IsStuffOrReadOnlyPermission,)


class StepCodeViewSet(viewsets.ModelViewSet):
    queryset = StepCode.objects.all()
    serializer_class = StepCodeSerializer
    filter_class = StepCodeFilter
    permission_classes = (IsStuffOrReadOnlyPermission,)
