from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teams.models import Team

from .forms import TeamForm


@login_required
def detail(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)

    return render(request, 'teams/detail.html', {
        'team': team
    })

@login_required
def teams_edit(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()
    
            messages.success(request, 'The changes was saved.')

            return redirect('myaccount')
    else:
        form = TeamForm(instance=team)

    return render(request, 'teams/teams_edit.html', {
        'team': team,
        'form': form
    })
