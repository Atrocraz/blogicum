from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path(
        '<int:id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path('<int:id>/comment/', views.add_comment, name='add_comment'),
    path(
        '<int:id>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        '<int:id>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    )
]

profile_urls = [
    path(
        'edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        '<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    )
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
    path('posts/', include(posts_urls)),
    path('profile/', include(profile_urls)),
]
