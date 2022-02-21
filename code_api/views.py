import os, random, json
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
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
from result_api.models import Result


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
        # コードの取得
        queryset = self.get_queryset()
        code = queryset.get(id=pk)
        if not code:  # チェック
            return Response({"detail": "リソースが見つかりません。"}, status.HTTP_400_BAD_REQUEST)

        # コードをランダムに３件取得
        try:
            other_codes = [
                queryset.get(id=uuid[0])
                for uuid in random.sample(list(queryset.values_list("id")), 3)
            ]
        except ValueError:
            return Response({"detail": "コードのリソース数が足りません。"}, status.HTTP_400_BAD_REQUEST)
        codes = [code, *other_codes]  # シミュレーションを実行するプログラム

        # シミュレータ実行
        result_data = {"result": "done"}

        # resultモデルへ結果を格納
        result = Result.objects.create(json_path="dummy", step=code.step)
        result.codes.set(codes)
        json_directory = "/tmp/result"
        json_filename = f"{json_directory}/{result.id}.json"
        result.json_path = json_filename
        result.save()

        # シミュレーション結果ファイルの保存
        os.makedirs("/tmp/result/", exist_ok=True)
        with open(json_filename, "x", encoding="UTF-8") as wf:
            wf.write(json.dumps(result_data))

        # 戻り値の準備
        unity_url = "http://Unity.com/"
        json_id = result.id

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
