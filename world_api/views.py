from rest_framework import viewsets

from .models import World
from .serializer import WorldSerializer
from .filter import WorldFilter


class WorldViewSet(viewsets.ModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
    filter_class = WorldFilter
