from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView
)
from django.utils import timezone
from django.urls import reverse

from blog.models import Category, Post, User
from blog.forms import CommentForm, PostCreateForm, UserEditForm
from core.classes import CommentBaseClass, PostEditDeleteClass


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
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


def post_detail(request, id):
    template = 'blog/detail.html'

    post = get_object_or_404(
        Post.objects.all().select_related('category', 'location', 'author')
        .filter(pk=id)
    )
    if (post.is_published is False
        or post.category.is_published is False
            or post.pub_date > timezone.now()) and post.author != request.user:
        raise Http404

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author')
    }

    return render(request, template, context)


class PostUpdateView(LoginRequiredMixin, PostEditDeleteClass, UpdateView):
    form_class = PostCreateForm


class PostDeleteView(LoginRequiredMixin, PostEditDeleteClass, DeleteView):

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfileDetailView(ListView):
    template_name = "blog/profile.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context

    def get_queryset(self) -> QuerySet[Any]:
        self.author = get_object_or_404(User, username=self.kwargs['username'])

        if self.author != self.request.user:
            return Post.published.all().filter(
                author=self.author,
                pub_date__lte=timezone.now()
            )

        return Post.objects.all().filter(
            author=self.author
        ).annotate(
            comment_count=models.Count('comments')
        ).order_by(
            '-pub_date'
        ).prefetch_related('location', 'category', 'author')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CategoryListView(ListView):
    model = Post

    template_name = "blog/category.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self) -> QuerySet[Any]:
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.published.all().filter(
            category__slug=self.category.slug
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


class CommentUpdateView(LoginRequiredMixin, CommentBaseClass, UpdateView):
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, CommentBaseClass, DeleteView):
    pass
