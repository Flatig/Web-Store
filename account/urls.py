from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_base, name='account_menu'),
    path('register/', views.register, name='registration'),
    path('register/done/<int:user_id>/', views.register_done, name='register_done'),
    path('login/', views.account_login, name='login'),
    path('profile:<str:username>/', views.profile, name='profile'),
    path('profile:<str:username>/edit/', views.edit, name='edit'),
    path('logout/', views.account_logout, name='logout'),
    # registration urls based on django.contrib.auth
    path('registration-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('registration-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('registration-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('registration-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('registration-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('registration-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
