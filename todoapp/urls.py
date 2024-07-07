from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns =[
    path('',views.home,name='home-page'),
    path('register/',views.register,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete-task'),
    path('update-task/<int:id>/', views.Update, name='update-task'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='todoapp/reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='todoapp/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='todoapp/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='todoapp/reset_complete.html'), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
  
]