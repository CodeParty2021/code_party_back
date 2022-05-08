from django.urls import path
from .views import FirebaseAuthView, UserRetrieveView, DisplayNameUpdateView


urlpatterns = [
    path("auth/", FirebaseAuthView.as_view()),
    path("update/<pk>/", DisplayNameUpdateView.as_view()),
    path("<pk>/", UserRetrieveView.as_view()),
]
