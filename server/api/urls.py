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

    #item stuff
    path('item/create/', ItemCreateView.as_view(), name='item-create'),
    path('item/list/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDeleteView.as_view(), name='item-delete'),

    #subscription stuff
    path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscription/list/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscription/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
    path('subscription/<int:pk>/add-item/', SubscriptionItemAddView.as_view(), name='subscription-item-add'),
    path('subscription/<int:pk>/remove-item/', SubscriptionItemRemoveView.as_view(), name='subscription-item-remove'),
    path('subscription/<int:pk>/list-items/', SubscriptionItemListView.as_view(), name='subscription-item-list'),

    #order stuff
    path('subscription/order/', OrderCreateView.as_view(), name='order-create'),
    path('subscription/<int:pk>/order/<int:order_pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/paid', OrderPaidView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/shipped', OrderShippedView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/delivered', OrderDeliveredView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/cancelled', OrderCancelledView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/list/', OrderListView.as_view(), name='order-list'),
]