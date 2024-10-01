from .views import get, create
from django.urls import path

urlpatterns = [
    path("get/", get.GetOwnerPayments.as_view(),name='get_payments'),
    path('get/<str:id>/', get.GetClientPayment.as_view(), name="get_payment"),
    path('create/<str:id>/', create.CreatePayment.as_view(),name='create_payment'),
    path('create/', create.OwnerCreatePayment.as_view(),name='owner_create_payment'),
    
]