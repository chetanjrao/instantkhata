from django.urls import path
from django.conf.urls import url
from .views import AuthManager

urlpatterns = [
    path('signin/', AuthManager.as_view(), name='signin')
]