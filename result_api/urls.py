from rest_framework import routers

from .views import ResultRetrieveView


router = routers.DefaultRouter()
router.register(r"", ResultRetrieveView)
urlpatterns = router.urls
