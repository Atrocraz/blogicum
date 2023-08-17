from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_list_or_404
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Post


User = get_user_model()


class PostsListView(ListView):
    model = Post

    template_name = "blog/index.html"
    paginate_by = 10


def create_post(request):
    pass


class ProfileDetailView(DetailView):
    model = User

    template_name = "blog/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_full_name'] = User.name
        return context


def post_detail(request, id):
    template = 'blog/detail.html'

    post = get_object_or_404(
        Post.published.all().select_related('category', 'location')
        # Post.published.published().select_related('category', 'location')
        .filter(pk=id)
    )
    context = {'post': post}

    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
        ), slug=category_slug
    )
    post_list = get_list_or_404(
        Post.published.all().filter(category__slug=category_slug)
        # Post.published.published().filter(category__slug=category_slug)
    )
    context = {
        'category': category,
        'post_list': post_list
    }

    return render(request, template, context)
