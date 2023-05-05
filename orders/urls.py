from django.urls import path
from .views import OrdersView

urlpatterns = [
    path("orders/", OrdersView.as_view()),
    # path("products/<int:pk>", ProductViewDetail.as_view()),
]
