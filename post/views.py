from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.all()
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm
        return redirect('main-post-view')

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }
    return render(request, 'main.html', context)


def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        prrofile = Profile.objects.get(user=user)
        if prrofile in post_obj.liked.all():
            post_obj.liked.remove(prrofile)
        else:
            post_obj.liked.add(prrofile)
        like, created = Like.objects.get_or_create(user=prrofile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        return redirect('main-post-view')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user==self.request.user:
            messages.warning(self.request,'Bu gonderiyi silmek icin yetkin yok Bilader')
        return obj


class PostUpdateView(UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'update.html'
    success_url = reverse_lazy('main-post-view')
    def form_valid(self, form):
        profile=Profile.objects.get(user=self.request.user)
        if form.instance.author==profile:
            return super().form_valid(form)
        else:
            form.add_error(None,'Bu gonderiyi goruntulemek icin yetkiniz yok')
            return super().form_invalid(form)