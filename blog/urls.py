from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'blog'
urlpatterns = [
    path('', views.PostView.as_view(), name = 'home'),
    path('posts/<slug:slug>/', views.PostDetails.as_view(), name='post_details'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password-reset/', views.ResetPassword.as_view(), name='password_reset'),
    path('accounts/password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('blog:password_reset_complete')), name = "password_reset_confirm"),
    path('accounts/password-reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('account/', views.PasswordChange.as_view(), name='account')
]