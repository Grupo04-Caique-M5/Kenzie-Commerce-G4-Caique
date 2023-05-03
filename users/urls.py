from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("refresh/", jwt_views.TokenRefreshView.as_view()),
]
