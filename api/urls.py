from rest_framework import routers
from .views import StageViewSet


router = routers.DefaultRouter()
router.register(r"stages", StageViewSet)
