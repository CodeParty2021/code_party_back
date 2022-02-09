from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .auth import FirebaseAuthentication
from .serializers import UserSerializer, UserReadonlySerializer
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
