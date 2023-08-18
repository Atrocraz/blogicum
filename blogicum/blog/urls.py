from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug', views.CategoryListView.as_view(), name='category_posts'),
    #path('category/<slug:category_slug>/',
    #     views.category_posts, name='category_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('profile/<slug:username>/', views.ProfileDetailView.as_view(), name='profile'),
]
