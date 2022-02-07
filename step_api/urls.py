from rest_framework import routers
from .views import StepViewSet


router = routers.DefaultRouter()
router.register(r"", StepViewSet)
urlpatterns = router.urls