from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.core.paginator import Paginator
from datetime import datetime
from blog.models import Category, Post
from blog.forms import UserEditForm, PostCreateForm, PostEditForm
from django.core.exceptions import PermissionDenied


User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Post.published.all().order_by('-pub_date')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    success_url = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


def post_detail(request, id):
    template = 'blog/detail.html'

    post = get_object_or_404(
        Post.published.all().select_related('category', 'location')
        .filter(pk=id)
    )
    context = {'post': post}

    return render(request, template, context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        if self.kwargs.get("author") != self.request.user:
            return PermissionDenied

        return Post.objects.get(id=self.kwargs.get("id"))

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'id': self.kwargs.get("id")}
        )


class ProfileDetailView(DetailView):
    model = User
    template_name = "blog/profile.html"
    slug_url_kwarg = 'username'
    slug_field = 'username'
    сontext_object_name = 'profile'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        page_num = self.request.GET.get('page')
        post_list = ''

        if author != self.request.user:
            post_list = Post.published.all().filter(
                author=author,
                pub_date__lte=datetime.today().strftime('%Y-%m-%d')
            ).order_by('-pub_date')

        else:
            post_list = Post.objects.all().filter(
                author=author
            ).order_by('-pub_date').annotate(
                comment_count=models.Count('comments')
            )

        paginator = Paginator(post_list, 10)
        context['page_obj'] = paginator.get_page(page_num)
        context['profile'] = author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CategoryListView(ListView):
    model = Post

    template_name = "blog/category.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.published.all().filter(
            category__slug=category.slug
        ).order_by('-pub_date')
