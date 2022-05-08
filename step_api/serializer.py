from rest_framework import serializers

from .models import Step, StepCode


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"


class StepCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepCode
        fields = "__all__"
