from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,DownloadRequest
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



@login_required
def send_request(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    print(post.author)
    if request.method == 'POST':
        download_request = DownloadRequest(requester=request.user, post=post)
        download_request.save()
        messages.success(request, 'Your download request has been sent.')  # Correct usage of messages.success()
        return redirect('post-detail', pk=post_id)
    else:
        return render(request, 'blog/send_request.html', {'post': post})

    
@login_required
def view_requests(request):
    
    user_requests = DownloadRequest.objects.filter(post__author=request.user)
    return render(request, 'blog/view_request.html', {'user_requests': user_requests})

@login_required
def requests(request):
    user_requests = DownloadRequest.objects.filter(requester=request.user)
    return render(request, 'blog/view_request.html', {'user_requests': user_requests})

@login_required
def approve_request(request, request_id):
    download_request = get_object_or_404(DownloadRequest, pk=request_id)
    if request.user == download_request.post.author:
        download_request.status = DownloadRequest.APPROVED
        download_request.save()
        messages.success(request, 'Download request approved.')
    else:
        messages.error(request, 'You are not authorized to approve this request.')
    return redirect('view-requests')

@login_required
def decline_request(request, request_id):
    download_request = get_object_or_404(DownloadRequest, pk=request_id)
    if request.user == download_request.post.author:
        download_request.status = DownloadRequest.DECLINED
        download_request.save()
        download_request.delete()  # Delete the request after declining
        messages.success(request, 'Download request declined and deleted.')
    else:
        messages.error(request, 'You are not authorized to decline this request.')
    return redirect('view-requests')


