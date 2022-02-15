from rest_framework import routers

from .views import ProgrammingLanguageViewSet, CodeViewSet


router = routers.SimpleRouter()
router.register(r"programminglanguage", ProgrammingLanguageViewSet)
router.register(r"", CodeViewSet)
urlpatterns = router.urls
