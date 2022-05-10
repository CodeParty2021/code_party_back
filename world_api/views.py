from rest_framework import viewsets

from .models import World
from .serializer import WorldSerializer
from .filter import WorldFilter
from .permission import IsStuffOrReadOnlyPermission


class WorldViewSet(viewsets.ModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
    filter_class = WorldFilter
    permission_classes = (IsStuffOrReadOnlyPermission,)
