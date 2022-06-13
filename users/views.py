from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.http import HttpResponse, Http404
from .auth import FirebaseAuthentication
from .serializers import UserSerializer, UserReadonlySerializer, UserUpdateSerializer
from .models import User


class FirebaseAuthView(APIView):
    authentication_classes = [
        FirebaseAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        user_serializer = UserSerializer(request.user)  # オブジェクトをjsonに変えるシリアライズ機能だけ使う
        # 結果を返す
        return Response({"userInfo": user_serializer.data, **request.auth})


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadonlySerializer


class DisplayNameUpdateView(UpdateAPIView):
    """
    説明を書く
    """
    authentication_classes = [
        FirebaseAuthentication,
    ]
    serializer_class = UserUpdateSerializer
    lookup_field = "id"
    queryset = User.objects.all()

    def get_object(self):
        try:
            instance = self.queryset.get(id=self.request.user.id)
            return instance
        except User.DoesNotExist:
            raise Http404
