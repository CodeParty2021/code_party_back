from django_filters import rest_framework as filters

from .models import Step, StepCode


class StepFilter(filters.FilterSet):
    index = filters.NumberFilter()
    order_by = filters.OrderingFilter(fields=(("index", "index"),))
    stage = filters.NumberFilter(field_name="stage__id", lookup_expr="contains")

    class Meta:
        model = Step
        fields = ()


class StepCodeFilter(filters.FilterSet):
    class Meta:
        model = StepCode
        fields = ["step"]
