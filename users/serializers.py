from rest_framework import serializers
from .models import User
from firebase_admin import auth


class UserSerializer(serializers.ModelSerializer):
    # 属性は変えるっぽい
    class Meta:
        model = User
        fields = "__all__"
