from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('media/Files/<int:pk>',PostDeleteView.as_view(),name='post-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),
    path('send-request/<int:post_id>/', views.send_request, name='send-request'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve-request'),
    path('view-requests/', views.view_requests, name='view-requests'),
    path('requests/', views.requests, name='requests'),
    path('decline-request/<int:request_id>', views.decline_request, name='decline-request'),
]
