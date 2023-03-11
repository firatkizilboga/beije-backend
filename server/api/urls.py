#api urls

from django.urls import path
from .views import *

urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='user-create'),
]