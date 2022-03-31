import os
import random
import json

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
from .permission import IsStaffOrReadOnlyPermission
from .filter import CodeFilter
from result_api.models import Result
from game_libs import sqare_paint


class ProgrammingLanguageViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingLanguage.objects.all()
    serializer_class = ProgrammingLanguageSerializer
    permission_classes = (IsStaffOrReadOnlyPermission,)


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission,)
    filter_class = CodeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[])
    def run(self, request, pk=None):
        MAX_PLAYER = 4
        queryset = self.get_queryset()
        codeids = [pk]  # リソースのIDをシミュレーション対象コードに追加する
        step = None
        try:
            step = queryset.get(id=pk).step
        except:
            return Response({"detail": "不正なIDです。"}, status.HTTP_400_BAD_REQUEST)

        # GETパラメータに指定されたコードを取得
        for i in range(1, MAX_PLAYER):
            if f"p{i}" in request.GET:
                codeids.append(request.GET.get(f"p{i}"))

        # コードを4件になるまでランダムに補充
        try:
            allCodes = set(
                [
                    uuid[0].urn[9:]
                    for uuid in queryset.filter(step=step).values_list("id")
                ]
            )
            allCodes = allCodes - set(codeids)
            codeids.extend(random.sample(
                list(allCodes), MAX_PLAYER - len(codeids)))
        except ValueError:
            return Response({"detail": "コードのリソース数が足りません。"}, status.HTTP_400_BAD_REQUEST)

        codes = [code, *other_codes]  # シミュレーションを実行するプログラム
        codes_str = [c.code_content for c in codes]
        # コードを関数オブジェクト化
        python_objects = []
        for code_str in codes_str:
            print(code_str)
            exec(code_str, globals())
            python_objects += [select]

        # シミュレータ実行
        option = sqare_paint.Option(user_code=python_objects)
        result_data = sqare_paint.start(option)
        # resultモデルへ結果を格納
        result = Result.objects.create(json_path="dummy", step=codes[0].step)
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
        unity_url = "http://localhost:3000/unity/sp/"
        json_id = result.id

        serializer = CodeRunResultSerializer(
            data={
                "unityURL": unity_url,
                "json_id": json_id,
                "json": result_data
            }
        )

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
