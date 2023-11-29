from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm


from .models import UserProfile
from teams.models import Team

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            team = Team.objects.create(name='The team name', created_by=request.user)
            team.members.add(request.user)
            team.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user)[0]

    return render(request, 'userprofile/myaccount.html', {
        'team': team
    })