from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # 属性は変えるっぽい
    class Meta:
        model = User
        fields = "__all__"


class UserReadonlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "display_name", "picture", "is_stuff")
