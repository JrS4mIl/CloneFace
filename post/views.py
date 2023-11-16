from django.shortcuts import render,redirect
from .models import Post,Like
from profiles.models import Profile

# Create your views here.
def post_comment_create_and_list_view(request):
    profile=Profile.objects.get(user=request.user)
    qs=Post.objects.all()
    context={
        'qs':qs,
        'profile':profile
    }
    return render(request,'main.html',context)

def like_unlike_post(request):
    user=request.user
    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        prrofile=Profile.objects.get(user=user)
        if prrofile in post_obj.liked.all():
            post_obj.liked.remove(prrofile)
        else:
            post_obj.liked.add(prrofile)
        like,created=Like.objects.get_or_create(user=prrofile,post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

        return redirect('main-post-view')


