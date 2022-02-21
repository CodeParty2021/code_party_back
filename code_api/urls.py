from rest_framework import routers

from .views import ProgrammingLanguageViewSet, CodeViewSet


router = routers.DefaultRouter()
router.register(r"programminglanguage", ProgrammingLanguageViewSet)
router.register(r"", CodeViewSet)
urlpatterns = router.urls
