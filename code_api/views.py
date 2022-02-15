from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ProgrammingLanguage, Code
from .serializer import (
    ProgrammingLanguageSerializer,
    CodeSerializer,
    CodeRunResultSerializer,
)
from .permission import IsOwnerOrReadOnlyPermission
from .filter import CodeFilter


class ProgrammingLanguageViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingLanguage.objects.all()
    serializer_class = ProgrammingLanguageSerializer


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission,)
    filter_class = CodeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[])
    def run(self, request, pk=None):
        # シミュレータの実行
        print(f"{pk} is being simulated!")

        # resultモデルへ結果を格納

        # 戻り値の準備
        unity_url = "http://Unity.com/"
        json_id = "f0ea866e-27b8-4217-8bba-deea776b7adc"

        serializer = CodeRunResultSerializer(
            data={
                "unityURL": unity_url,
                "json_id": json_id,
            }
        )

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
