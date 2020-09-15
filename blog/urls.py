from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import LoginForm

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
    path('accounts/password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('account/', views.AccountSettings.as_view(), name='account'),
    path('account/add-post/', views.AddPost.as_view(), name='add_post'),
    path('account/edit-post/<slug:slug>/', views.EditPost.as_view(), name='edit_post'),
    path('account/delete-post/<slug:slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('account/my-posts/', views.MyPostsView.as_view(), name = 'my_posts'),
    path('category/<str:category>/', views.Categories, name='category'),
    path('like/<slug:slug>', views.Like, name='like_post')
]