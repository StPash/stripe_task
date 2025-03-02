from django.urls import path

from store.views.get_buy_item_views import buy_item_view, get_item_view
from store.views.get_buy_order_views import buy_order_view, get_order_view

urlpatterns = [
    path('buy/<int:item_id>/', buy_item_view, name='buy_item'),
    path('item/<int:item_id>/', get_item_view, name='get_item'),
    path('buy_order/<int:order_id>/', buy_order_view, name='buy_order'),
    path('order/<int:order_id>/', get_order_view, name='get_order'),
]
