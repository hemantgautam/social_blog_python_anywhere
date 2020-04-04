from django.urls import path
from . import views
from .views import PostListView, \
                    PostDetailView, \
                    PostCreateView, \
                    PostUpdateView, \
                    PostDeleteView, \
                    UserPostListView, \
                    PostUnPublishedListView


urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-details'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/draft/', PostUnPublishedListView.as_view(), name='post-draft'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/publish', views.post_publish_unpublish, name='post-publish'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
]