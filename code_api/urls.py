from rest_framework import routers

from .views import CodeViewSet


router = routers.DefaultRouter()
router.register(r"", CodeViewSet)
urlpatterns = router.urls
