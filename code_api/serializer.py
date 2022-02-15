from rest_framework import serializers

from .models import Code


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class CodeRunResultSerializer(serializers.ModelSerializer):
    unity_url = serializers.URLField()
    json_id = serializers.IntegerField()