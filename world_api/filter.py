from django_filters import rest_framework as filters

from .models import World


class WorldFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    index = filters.NumberFilter()

    order_by = filters.OrderingFilter(fields=(("index", "index"),))

    class Meta:
        model = World
        fields = ()
