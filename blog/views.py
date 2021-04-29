from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView, DeleteView, CreateView, UpdateView
from .forms import PostForm, CommentForm
from .models import Post
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 1



class PostDetailView( FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_connected = self.get_object()
        self.object.author = self.request.user

        self.object.save()
        return super().form_valid(form)




class PostCreateView(CreateView):
    model = Post
    template_name = 'create.html'
    form_class = PostForm
    success_url = reverse_lazy('post_detail')

    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'create.html', {'form': form})

    def get_context_data(self, **kwargs):
        kwargs['post_detail'] = Post.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = '/'
class PostEditView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('post_detail')

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'post_edit.html', {'form': form})


class SearchResultsView(View):
    def get(self, request):
        search_param = request.GET.get('q')
        results = Post.objects.filter(Q(title__icontains=search_param) | Q(text__icontains=search_param))

        # select * from product where title ilike ' '  or description ilike ' '
        return render(request, 'search_results.html', locals())
