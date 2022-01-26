from dataclasses import fields
from django_filters import rest_framework as filters

from .models import Stage


class StageFilter(filters.FilterSet):
    stage_index = filters.NumberFilter()
    order_by = filters.OrderingFilter(fields=(("index", "index"),))
    world = filters.NumberFilter(field_name="world__id", lookup_expr="contains")

    class Meta:
        model = Stage
        fields = []
