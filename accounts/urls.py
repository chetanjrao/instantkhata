from django.urls import path
from django.conf.urls import url
from .views import AuthManager, OTPManager, UserManager, EditProfileView

urlpatterns = [
    path('profile/', UserManager.as_view(), name='profile'),
    path('signin/', AuthManager.as_view(), name='signin'),
    path('signin/verify/', OTPManager.as_view(), name='verify'),
    path('profile/edit/', EditProfileView.as_view(), name='edit')
]