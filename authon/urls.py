from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register_user,name='register'),
    path('delete/<int:id>',views.delete_user,name='delete_user'),
    path('getuser/<int:id>',views.get_user_by_id,name='get_user_by_id'),
    path('profile/',views.get_user_profile,name='get_user_profile'),
    path('getallusers/',views.get_all_users,name='get_all_users'),
    path('updateuser/<int:id>',views.update_user,name='update_user'),
    path('updateprofile/',views.updateUserProfile,name='updateUserProfile'),
]
