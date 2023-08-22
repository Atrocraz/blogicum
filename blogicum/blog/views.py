from typing import Any, Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from datetime import datetime
import pytz
from blog.models import Category, Post
from blog.forms import UserEditForm, PostCreateForm, PostEditForm, CommentForm
from core.classes import CommentBaseClass


User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Post.published.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

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
        Post.objects.all().select_related('category', 'location')
        .filter(pk=id)
    )
    if (post.is_published is False
        or post.category.is_published is False
            or post.pub_date > pytz.UTC.localize(datetime.now())):
        if post.author != request.user:
            raise Http404

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author')
    }

    return render(request, template, context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'blog/create.html'
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=kwargs['id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', id=kwargs['id'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'id': self.kwargs.get("id")}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=kwargs['id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
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
                pub_date__lte=pytz.UTC.localize(datetime.now())
            )

        else:
            post_list = Post.objects.all().filter(
                author=author
            ).annotate(
                comment_count=models.Count('comments')
            ).order_by('-pub_date')

        paginator = Paginator(post_list, 10)
        context['page_obj'] = paginator.get_page(page_num)
        context['profile'] = author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=kwargs['username'])
        print(instance.username)
        if instance != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
        )


@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=id)


class CommentUpdateView(CommentBaseClass, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentBaseClass, DeleteView):
    pass
