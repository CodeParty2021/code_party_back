from dataclasses import field
from rest_framework import serializers

from .models import ProgrammingLanguage, Code


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = "__all__"


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = (
            "id",
            "code_content",
            "created_at",
            "updated_at",
            "language",
            "step",
            "user",
        )
        read_only_fields = ("created_at", "updated_at", "user")


class CodeRunResultSerializer(serializers.Serializer):
    unityURL = serializers.URLField()
    json_id = serializers.UUIDField()

    # class Meta:
    #     fields = (
    #         "unity_url",
    #         "json_id",
    #     )
