from rest_framework import routers
from .views import TestModelViewSet


router = routers.DefaultRouter()
router.register(r"testmodels", TestModelViewSet)
