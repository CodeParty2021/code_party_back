from rest_framework import serializers

from .models import Code, Result, ResultCode

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('name', 'user', 'file_path','created_date','language')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('id', 'json_path', 'language')

class ResultCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultCode
        fields = ('result', 'code')

