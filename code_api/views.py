import os
import random
import json

from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .models import ProgrammingLanguage, Code
from .serializer import (
    CodeTestSerializer,
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


def execute_code(codes):
    codes_str = [c.code_content for c in codes]
    # コードを関数オブジェクト化
    python_objects = []
    for code_str in codes_str:
        user_dict = {}
        exec(code_str, user_dict)
        try:
            python_objects += [user_dict["select"]]
        except NameError:
            raise NameError()
    # ユーザー取得
    players = []

    for code_item in codes:
        auther = code_item.user
        players += [{"icon": auther.picture, "name": auther.display_name}]

    # シミュレータ実行
    option = sqare_paint.Option(user_code=python_objects, players=players)
    result_data = sqare_paint.start(option)

    return result_data


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission,)
    filter_class = CodeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[])
    def test(self, request, pk=None):
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
            codeids.extend(random.sample(list(allCodes), MAX_PLAYER - len(codeids)))
        except ValueError:
            return Response({"detail": "コードのリソース数が足りません。"}, status.HTTP_400_BAD_REQUEST)

        # コードを取得
        codes = []
        try:
            for codeid in codeids:
                codes.append(
                    queryset.get(id=codeid, step=step)
                )  # 指定されたコードが同じステップのものかを取得
        except:
            return Response({"detail": "リソースが見つかりません。"}, status.HTTP_400_BAD_REQUEST)

        try:
            result_data = execute_code(codes)
        except NameError:
            return Response(
                {"detail": "select関数が見つかりません。"}, status.HTTP_400_BAD_REQUEST
            )
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

        serializer = CodeTestSerializer(
            data={"unityURL": unity_url, "json": result_data}
        )

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[])
    def run(self, request):
        # コードの取得\
        queryset = self.get_queryset()
        post_code = dict(request.data)["code"]
        codes = []
        step = None
        if len(post_code) == 0:
            return Response({"detail": "codeが指定されていません。"}, status.HTTP_400_BAD_REQUEST)

        try:
            step = queryset.get(id=post_code[0]).step
        except:
            return Response({"detail": "不正なIDです。"}, status.HTTP_400_BAD_REQUEST)
        for pid in post_code:
            code = queryset.get(id=pid)
            if not code:  # チェック
                return Response(
                    {"detail": "リソースが見つかりません。"}, status.HTTP_400_BAD_REQUEST
                )
            codes += [code]

        # 4つじゃなかったらランダムに足す
        if len(codes) <= 4:
            try:
                codes += [
                    queryset.get(id=uuid[0])
                    for uuid in random.sample(
                        list(queryset.filter(step=step).values_list("id")),
                        4 - len(codes),
                    )
                ]
            except ValueError:
                return Response(
                    {"detail": "コードのリソース数が足りません。"}, status.HTTP_400_BAD_REQUEST
                )

        # コード実行
        result_data = None
        try:
            result_data = execute_code(codes)
        except NameError:
            return Response(
                {"detail": "select関数が見つかりません。"}, status.HTTP_400_BAD_REQUEST
            )

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
        unity_url = "http://localhost:3000/unity/sp/"
        json_id = result.id

        serializer = CodeRunResultSerializer(
            data={"unityURL": unity_url, "json_id": json_id, "json": result_data}
        )

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
