from django_filters import rest_framework as filters

from .models import Result


class ResultFilter(filters.FilterSet):
    step = filters.NumberFilter(field_name="step__id")

    order_by = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
        )
    )

    class Meta:
        model = Result
        fields = ()
