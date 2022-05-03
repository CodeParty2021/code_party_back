from django.urls import path
from .views import FirebaseAuthView, UserRetrieveView, DisplayNameUpdateView


urlpatterns = [
    path("auth/", FirebaseAuthView.as_view()),
    path("<pk>/", UserRetrieveView.as_view()),
    path("displayname_update/<str:pk>/", DisplayNameUpdateView.as_view()),
]
