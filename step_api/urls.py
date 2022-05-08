from rest_framework import routers
from .views import StepCodeViewSet, StepViewSet


router = routers.DefaultRouter()
router.register(r"", StepViewSet)
router.register(r"codes", StepCodeViewSet)
urlpatterns = router.urls
