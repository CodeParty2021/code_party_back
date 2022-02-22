from rest_framework import routers

from .views import ResultViewSet


router = routers.DefaultRouter()
router.register(r"", ResultViewSet)
urlpatterns = router.urls
