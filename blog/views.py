from django.shortcuts import render, get_object_or_404
from .models import Posts
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )

# @login_required
# def home(request):
#     context = {'posts':Posts.objects.all()}
#     return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
    model = Posts
     # by default a class view will look for template as <app>/<model>_<viewtype.html>
     # but we can specify our own template path as
    template_name = 'blog/home.html'
     # by default a Listview will look for take list as name object_list
     # but we can specify our own name as
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'blog/user_posts.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post_args = self.get_object()
        if self.request.user == post_args.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/blog'

    def test_func(self):
        post_args = self.get_object()
        if self.request.user == post_args.author:
            return True
        return False


@login_required
def about(request):
    return render(request, 'blog/about.html')

@login_required
def contact(request):
    return render(request, 'blog/contact.html')
