#api urls

from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
]