from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin

from .models import Post, PostComment
from django.contrib import messages
from django.views.generic import ListView, \
    DetailView, \
    CreateView, \
    UpdateView, \
    DeleteView, \
    FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm


# function view
# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#         'title': 'home',
#     }
#     return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_queryset(self):
        return Post.objects.filter(published=True).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(published=True, author=user).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = PostComment.objects.all()
        # context['form'] = CommentForm()
        context['form'] = CommentForm()
        return context

    #
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            User.comment_user = self.request.user  # to add the user
            # post = Post()
            Post.post_id = Post.objects.filter(pk=self.kwargs.get('pk'))
            # PostComment.post_id = 16
            # comment.post_id = Post.post_id
            # postid = PostComment.objects.filter(pk=self.kwargs.get('pk'))
            # comment.post_id = postid
            comment.save()
            # return redirect('detail')  # add your url


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def post_publish_unpublish(request, post_id):
    try:
        # Updating the published column of item to True
        item = Post.objects.get(pk=post_id, author=request.user.id)
        if item.published:
            item.published = False
        else:
            item.published = True
        item.save()
        messages.success(request, 'Post is Published')
        return redirect('post-unpublished')
    except:
        return redirect('blog-home')


# class PostPublishUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
#     model = Post
#     # fields = ['published']
#
#     def form_valid(self, form):
#         self.Post = form.save(commit=False)
#         form.instance.author = self.request.us
#         self.Post.save()
#         return super(PostPublishUpdateView, self).form_valid(form)
#     # def form_valid(self, form):
#     #     form.instance.author = self.request.user
#     #     return super().form_valid(form)
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             # post_item = Post.objects.all()
#             post.published = True
#             # post_item.save()
#             return True
#         return False


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'published']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUnPublishedListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_queryset(self):
        user = self.request.user.id
        return Post.objects.filter(published=False, author_id=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(PostUnPublishedListView, self).get_context_data(**kwargs)
        context['draft_empty_text'] = "Draft Empty, No post to publish"
        return context


def about(request):
    return render(request, "blog/about.html", {'title': 'about'})
