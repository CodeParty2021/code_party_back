from rest_framework import routers
from .views import StageViewSet


router = routers.DefaultRouter()
router.register(r"Stage", StageViewSet)
urlpatterns = router.urls
