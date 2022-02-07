from rest_framework import serializers

from .models import Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"