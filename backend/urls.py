# your_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('dj_auth_package.urls')),
    path('payment/', include('payment.apis.urls')),
]
