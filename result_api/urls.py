# from django.urls import path

# from .views import ResultListView, ResultRetrieveView


# urlpatterns = [
#   path("<pk>/json/", ResultRetrieveView.as_view()),
#   path("<pk>/", ResultRetrieveView.as_view()),
#   path("", ResultListView.as_view()),
# ]

from rest_framework import routers

from .views import ResultViewSet


router = routers.DefaultRouter()
router.register(r"", ResultViewSet)
urlpatterns = router.urls
