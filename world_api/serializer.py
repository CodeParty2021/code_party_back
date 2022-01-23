from rest_framework import serializers
from .models import World


class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = "__all__"
