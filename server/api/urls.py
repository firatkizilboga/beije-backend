from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user-register'), #post requires email, first_name, last_name, password
    path('user/login/', UserLoginView.as_view(), name='user-login'), #post requires email, password
    path('admin/create/', AdminCreateView.as_view(), name='admin-create'), #post requires email, first_name, last_name, password

    path('address/create/', AddressCreateView.as_view(), name='address-create'), #post requires title, address_line1 optional address_line2, city, neighborhood, postal_code, country
    path('address/list/', AddressListView.as_view(), name='address-list'), #post
    path('address/<int:pk>/', AddressDetailView.as_view(), name='address-detail'), #post 
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'), #delete

    #item stuff
    path('item/create/', ItemCreateView.as_view(), name='item-create'), #post requires name and price
    path('item/list/', ItemListView.as_view(), name='item-list'), #get 
    path('item/<int:pk>/', ItemDeleteView.as_view(), name='item-delete'), #delete

    #subscription stuff
    path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription-create'), #post requires title, address, fufillment_frequency
    path('subscription/list/', SubscriptionListView.as_view(), name='subscription-list'), #post
    path('subscription/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'), #post
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription-delete'), #delete
    path('subscription/<int:pk>/add-item/', SubscriptionItemAddView.as_view(), name='subscription-item-add'), #post requires item_id and quantity
    path('subscription/<int:pk>/remove-item/', SubscriptionItemRemoveView.as_view(), name='subscription-item-remove'), #post requires item_id and quantity
    path('subscription/<int:pk>/list-items/', SubscriptionItemListView.as_view(), name='subscription-item-list'),

    path('subscription/<int:pk>/deactivate', SubscriptionDeactivateView.as_view(), name='subscription-activate'), #post
    path('subscription/<int:pk>/activate', SubscriptionActivateView.as_view(), name='subscription-deactivate'), #post

    #order stuff
    path('subscription/<int:pk>/order/create', OrderCreateView.as_view(), name='order-create'), #post
    path('subscription/<int:pk>/order/<int:order_pk>/', OrderDetailView.as_view(), name='order-detail'), #post
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/paid', OrderPayView.as_view(), name='order-paid'), #post requires admin user
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/shipped', OrderShipView.as_view(), name='order-shipped'), #post requires admin user
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/delivered', OrderDeliverView.as_view(), name='order-delivered'), #post requires admin user
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/cancelled', OrderCancelView.as_view(), name='order-cancelled'), #post
    path('subscription/<int:pk>/order/list/', OrderListView.as_view(), name='order-list'),  #post
]