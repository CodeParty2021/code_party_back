from rest_framework import routers
from .views import WorldViewSet


router = routers.DefaultRouter()
router.register(r"", WorldViewSet)
urlpatterns = router.urls
