from django_filters import rest_framework as filters

from .models import Stage

class StageFilter(filters.FilterSet):
  name = filters.CharFilter(field_name="name", lookup_expr="contains")
  index = filters.NumberFilter()

  order_by = filters.OrderingFilter(fields=(("index", "index"),))

  class Meta:
    model = Stage
    fields = ()