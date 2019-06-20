from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render

#forms
from .forms import PostForm, CommentForm
from .models import Post

#pagination
from django.core.paginator import Paginator


class HomePageView(ListView):
    model = Post
    template_name = 'gallerymain.html'
    context_object_name ='post_list'
    
    #pagination
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.all().order_by('-birthday')



class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'gallerypost.html'
    success_url = reverse_lazy('gallery_main')
    

class DetailPostView(DetailView):
    model = Post
    template_name = 'gallerydetail.html'


class DeletePostView(DeleteView):
    model = Post
    template_name='gallerydelete.html'
    success_url = reverse_lazy('gallery_main')

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'gallerypost.html'
    form_class = PostForm

    def get_absolute_url(self):
        return reverse('gallery_detail', kwargs={'pk': self.pk})

#comment
def gallerycomment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('gallery_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'galleryaddcomment.html', {'form': form})


    
        
    