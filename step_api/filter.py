from django_filters import rest_framework as filters

from .models import Step

class StepFilter(filters.FilterSet):
		# ここでフィルターフィールドを定義
		# 例
    # name = filters.CharFilter(field_name="name", lookup_expr="contains")
    # index = filters.NumberFilter()
    # order_by = filters.OrderingFilter(fields=(("index", "index"),))

    class Meta:
        model = Step
        fields = ()