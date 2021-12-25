from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer


class FirebaseAuthView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(
            raise_exceptions=True
        )  # validationerrorを返しますよということ、例外をライズっていうらしい
        serializer.save()
        return Response(serializer.data)
