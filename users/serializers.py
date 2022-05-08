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
        fields = ("id", "display_name", "picture", "is_staff")


class UserUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "display_name", "picture", "is_staff")
