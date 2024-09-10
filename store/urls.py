from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.get_all_products,name='all_products'),
    path('product/<int:pk>',views.get_product,name='get_product'),
    path('products/create/',views.create_product,name='create_product'),
    path('product/update/<int:pk>',views.update_product,name='update_product'),
    path('product/delete/<int:pk>',views.delete_product,name='delete_product'),
    path('product/upload_image/<int:pk>',views.upload_image ,name='upload_image'),
    path('products/search_products/<str:search_param>',views.search_products,name='search_products'),
    path('products/<int:pk>/update_review',views.update_review,name='update_review'),
    path('product/<int:pk>/delete_review',views.delete_review,name='delete_review'),
    path('getorder/<int:pk>',views.get_order_by_id,name='get_order_by_id'),
    path('updateordertopaid/<int:pk>',views.UpdateOrderToPaid,name='UpdateOrderToPaid'),
    path('updateordertodelievered/<int:pk>',views.UpdateOrderToDelievered,name='UpdateOrderToDelievered'),
    path('placeorder', views.addOrderItems, name='addOrderItems'),
    path('get_all_orders',views.get_all_orders,name='get_all_orders'),
    path('get_my_orders',views.get_my_orders,name='get_my_orders'),
    
]