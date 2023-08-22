from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path(
        'posts/<int:id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path('posts/<int:id>/comment/', views.add_comment, name='add_comment'),
    path(
        'posts/<int:id>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'posts/<int:id>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
]
