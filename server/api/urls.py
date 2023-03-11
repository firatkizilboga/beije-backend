#api urls

from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),

    path('address/create/', AddressCreateView.as_view(), name='address-create'),
    path('address/list/', AddressListView.as_view(), name='address-list'),
    path('address/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),

]