from django.urls import path
from .views import ProductView, ProductViewDetail

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<int:pk>", ProductViewDetail.as_view()),
]
