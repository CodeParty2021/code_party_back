import json, os
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Result
from .serializer import ResultSerializer
from .filter import ResultFilter


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_class = ResultFilter

    @action(detail=True, methods=["get"])
    def json(self, request, pk=None):
        object = Result.objects.get(id=pk)
        if not object:
            return Response({"message": "リソースが見つかりません。"}, status.HTTP_400_BAD_REQUEST)
        # jsonが存在するか確認
        if not os.path.exists(object.json_path):
            return Response({"message": "期限切れ。もう一度実行して下さい。"}, status.HTTP_404_NOT_FOUND)
        # json読込
        with open(object.json_path, "r") as f:
            data = json.load(f)
        return Response(data)
