from django.shortcuts import render
from .models import Profile,Relationship
from .forms import ProfileModelForm

# Create your views here.
def index(request):
    user = request.user
    hello = "Hello Word"
    context = {
        'user': user,
        'hello': hello
    }
    return render(request, 'index.html', context)


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form=ProfileModelForm(request.POST or None,request.FILES or None,instance=profile)
    confirm=False
    if request.method=='POST':
        if form.is_valid():
            form.save()
            confirm=True
    context = {
        'profile': profile,
        'form':form,
        'confirm':confirm,
    }
    return render(request, 'myprofile.html', context)

def invities_recived_view(request):
    profile=Profile.objects.get(user=request.user)
    qs=Relationship.objects.invatations_recived(profile)

    context={
        'qs':qs
    }
    return render(request,'my_invities.html',context)

def profile_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_profiles(user)

    context={
        "qs":qs
    }
    return render(request,'profile_list.html',context)

def invite_profiles_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_to_invate(user)
    context={"qs":qs}
    return render(request,"to_invite_list.html",context)
