import django_filters
from rest_framework import viewsets, filters

from .models import Code,Result,ResultCode
from .serializer import CodeSerializer,ResultSerializer,ResultCodeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class ResultCodeViewSet(viewsets.ModelViewSet):
    queryset = ResultCode.objects.all()
    serializer_class = ResultCodeSerializer


class CodeTestAPI(APIView):
#   authentication_classes = (authentication.TokenAuthentication,)
#    permission_classes = (permissions.IsAdminUser,)

    #テストように入れた
    def get(self, request, format=None):
        return Response({"message": "Hello World!!"},
            status=status.HTTP_200_OK)

    def post(self, request):
        #reqestからcodeをローカルに保存
        #codeレコード作成
        #シミュレータ実行
        #result,resultcodeレコードを作成
        #jsonをResponse
        return Response({'succeeded': True})