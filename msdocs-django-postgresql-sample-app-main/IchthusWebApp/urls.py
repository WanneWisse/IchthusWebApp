from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user',views.register_user,name="register_user"),
    path('login_user',views.login_user,name="login_user"),
    path('logout_user',views.logout_user,name="logout_user"),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('register_user_event', views.register_user_event, name='register_user_event'),
    path('deregister_user_event', views.deregister_user_event, name='deregister_user_event'),
    path('image_post', views.image_post, name='image_post'),
    path('change_paid/<int:tickie_id>/', views.change_paid, name='change_paid')
]