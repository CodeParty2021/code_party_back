from rest_framework import serializers
from .models import TestModel

class TestModelSerializer(serializers.ModelSerializer):
    """シリアライザー"""
    class Meta:
        model = TestModel
        fields = ('name', 'age')
