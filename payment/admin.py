from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentPanel (admin.ModelAdmin) : 
    list_display = ['user','amount','datetime','exp_at','id']