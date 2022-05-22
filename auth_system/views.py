
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
from .forms import UsernameForm

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.forms import LoginForm

# Add 'user' group to default user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='user'))



def editProfile(request):
    user = get_object_or_404(User, id=request.user.id)
    form = UsernameForm(request.POST or None, instance=user)
    if request.method == 'POST':
        form = UsernameForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
    context = {"form":form, 'user': user}
    return render(request, 'auth_system/edit_profile.html', context)




# HTMX

def changePassword(request):
    user = get_object_or_404(User, id=request.user.id)
    form = SetPasswordForm(user=user, data=request.POST)
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'partials/change_password.html', context)
