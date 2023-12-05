import datetime

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, Comment
from .forms import EditProfileForm, PostForm, AddCommentForm


class IndexView(ListView):
    template_name = 'blog/index.html'

    model = Post
    paginate_by = 10
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.get_published_posts()


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'

    model = Post
    paginate_by = 10
    context_object_name = 'page_obj'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']

        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True,
        )

        return Post.get_posts_by_category(category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )

        return context


class PostDetailView(ListView):
    template_name = 'blog/detail.html'

    model = Comment
    paginate_by = 10
    context_object_name = 'comments'

    def get_queryset(self):
        post = self.get_post(**self.kwargs)

        return Comment.objects.filter(post=post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = self.get_post(**kwargs)
        context['form'] = AddCommentForm()

        return context

    def get_post(self, **kwargs):
        id = self.kwargs['id']

        post = get_object_or_404(Post, id=id)

        if ((
                not post.is_published
                or not post.category.is_published
                # при написании post.pub_date > datetime.datetime.now()
                # выдаёт ошибку
                or datetime.datetime.combine
                (
                    post.pub_date.date(),
                    post.pub_date.time()
                ) > datetime.datetime.now())
                and self.request.user != post.author):
            raise Http404('Post does not exist')

        return post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    success_url = 'blog:profile'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user.username
            })


class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def get_object(self, queryset=None):
        id = self.kwargs['id']

        post = get_object_or_404(Post, id=id)

        return post

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['id'])

        if self.request.user != post.author:
            return redirect('blog:post_detail', id=self.kwargs['id'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'id': self.object.id
            })


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        id = self.kwargs['id']

        post = get_object_or_404(Post, id=id)

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = get_object_or_404(Post, id=self.kwargs['id'])
        context['form'] = PostForm(instance=post)

        return context

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['id'])

        if self.request.user != post.author:
            return redirect('blog:post_detail', id=self.kwargs['id'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user.username
            })


class AddCommentView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/comment.html'
    model = Comment
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'id': self.object.post.id
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, id=self.kwargs['id'])

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['id'])
        return super().form_valid(form)


class EditCommentView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/comment.html'
    model = Comment
    form_class = AddCommentForm

    def get_object(self, queryset=None):
        comment_id = self.kwargs['comment_id']

        comment = get_object_or_404(
            Comment,
            id=comment_id,
        )

        return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, id=self.kwargs['id'])

        return context

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])

        if self.request.user != comment.author:
            raise Http404('Post does not exist')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'id': self.object.post.id
            })


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        comment_id = self.kwargs['comment_id']

        comment = get_object_or_404(
            Comment,
            id=comment_id,
        )

        return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, id=self.kwargs['id'])

        return context

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])

        if self.request.user != comment.author:
            raise Http404('Post does not exist')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'id': self.object.post.id
            })


class ProfileView(ListView):
    template_name = 'blog/profile.html'

    model = Post
    paginate_by = 10
    context_object_name = 'page_obj'

    def get_queryset(self):
        username = self.kwargs['username']

        user_profile = get_object_or_404(
            User,
            username=username,
        )

        if user_profile is None:
            raise Http404('Profile does not exist')

        return Post.objects.filter(
            author=user_profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.kwargs['username']

        user_profile = get_object_or_404(
            User,
            username=username,
        )

        context['profile'] = user_profile

        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'blog/user.html'
    model = User
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user.username
            })
