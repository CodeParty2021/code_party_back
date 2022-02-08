import django_filters
from rest_framework import viewsets, filters

from .models import Step
from .serializer import StepSerializer
from .filter import StepFilter


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    filter_class = StepFilter
