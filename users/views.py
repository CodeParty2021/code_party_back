from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class FirebaseAuthView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=request.data)
