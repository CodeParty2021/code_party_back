from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Code
from .serializer import CodeSerializer, CodeRunResultSerializer
from .permission import IsOwnerOrReadOnlyPermission
from .filter import CodeFilter


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission,)
    filter_class = CodeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=["get"])
    def run(self, request, pk=None):
        # シミュレータの実行

        # 戻り値の準備
        unity_url = "Unity url"
        json_id = "json_id"

        serializer = CodeRunResultSerializer(data={
          "unityURL" : unity_url,
          "json_id" : json_id,
        })

        return Response(serializer.data)