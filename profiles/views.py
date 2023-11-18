from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

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
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'myprofile.html', context)


def invities_recived_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_recived(profile)
    result=list(map(lambda x:x.sender,qs))
    is_empty=False

    if len(result)==0:
        is_empty=True



    context = {
        'qs': result,
        'is_empty':is_empty,
    }
    return render(request, 'my_invities.html', context)


def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        "qs": qs
    }
    return render(request, 'profile_list.html', context)


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_to_invate(user)
    context = {"qs": qs}
    return render(request, "to_invite_list.html", context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'profile_list.html'

    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_re=Relationship.objects.filter(sender=profile)
        rel_es=Relationship.objects.filter(revicer=profile)
        rel_reciver=[]
        rel_sender=[]
        for item in rel_re:
            rel_reciver.append(item.revicer.user)
        for item in rel_es:
            rel_sender.append(item.sender.user)
        context['rel_receiver']=rel_reciver
        context['rel_sender'] = rel_sender
        context['is_empty']=False
        if len(self.get_queryset())==0:
            context['is_empty']=True
        return context

def send_invatation(request):
    if request.method=='POST':
        pk=request.POST.get('profile_pk')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)
        rel=Relationship.objects.create(sender=sender,revicer=receiver,status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')

def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get(Q(sender=sender)& Q(revicer=receiver)|Q(sender=receiver)&Q(revicer=sender))
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')

def accept_invatation(request):
    if request.method=='POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        if rel.status=='send':
            rel.status='accepted'
            rel.save()
        return redirect('my-invities-view')
def reject_invatation(request):
    if request.method=='POST':
        pk=request.POST.get('profile')
        sender=Profile.objects.get(user=request.user)
        receiver=Profile.objects.get(pk=pk)
        rel=get_object_or_404(Relationship,sender=sender,reciver=receiver)
        rel.delete()
    return redirect('my-invite-view')
