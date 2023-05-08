from django.urls import path
from .views import CartProductsView

urlpatterns = [
    path("cart/", CartProductsView.as_view()),
]
