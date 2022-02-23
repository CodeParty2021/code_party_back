from django_filters import rest_framework as filters

from .models import Code


class CodeFilter(filters.FilterSet):
    language = filters.CharFilter(field_name="language__name")
    step = filters.NumberFilter(field_name="step__id")
    user = filters.CharFilter(field_name="user__id")

    order_by = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        )
    )

    class Meta:
        model = Code
        fields = ()
