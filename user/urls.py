from django.urls import path
from .views import hello, LoginView , AdminHomeView, CustomerHomeView

urlpatterns = [
    path('', hello, name='hello'),
    path('login/', LoginView.as_view(), name="login"),
    path('admin-panel/', AdminHomeView, name="admin_panel"),
    path('customer-panel/', CustomerHomeView, name="customer_panel"),
]