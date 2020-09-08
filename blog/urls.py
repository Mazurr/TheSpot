from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('', views.PostView.as_view(), name = 'home'),
    path('<slug:slug>/', views.PostDetails.as_view(), name='post_details')
]