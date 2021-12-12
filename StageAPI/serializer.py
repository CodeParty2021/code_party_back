from rest_framework import serializers
from .models import Stage


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ("id", "name", "stage_index", "rule")
