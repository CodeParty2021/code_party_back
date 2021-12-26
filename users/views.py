from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from users.auth import FirebaseAuthentication
from users.models import User
from users.serializers import UserSerializer


class FirebaseAuthView(APIView):
    authentication_classes = [
        FirebaseAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        res = {"user_info": request.user, **request.auth}
        user_serializer = UserSerializer(request.user)  # オブジェクトをjsonに変えるシリアライズ機能だけ使う
        # 結果を返す
        return Response({"user_info": user_serializer.data, **request.auth})
