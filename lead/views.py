from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View

from .forms import AddCommentForm, AddFileForm
from .models import Lead
from client.models import Client, Comment as ClientComment
from teams.models import Team

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    
    def get_queryset(self):
        queryset = Lead.objects.filter(created_by = self.request.user, converted_to_client=False)
        return queryset


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = Lead.objects.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        return queryset
    
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')
    
    
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    fields = ['name', 'email', 'description', 'priority', 'status']
    success_url = reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit lead'
        return context
        
    

class LeadCreateView(LoginRequiredMixin, CreateView):
    model=Lead
    fields = ['name', 'email', 'description', 'priority', 'status']
    success_url = reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add lead'
        return context
        
    
    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()

        return redirect(self.success_url)
    

class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.lead_id = pk
            file.created_by = request.user
            file.save()
        
            return redirect('leads:detail', pk=pk)

            


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        form = AddCommentForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()


            return redirect('leads:detail', pk=pk)

# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by = request.user, converted_to_client=False)

#     return render(request, 'lead/leads_list.html', {
#         'leads': leads
#     })

# @login_required
# def leads_detail(request, pk):
#     # lead = Lead.objects.filter(created_by = request.user).get(pk=pk)
#     lead = get_object_or_404(Lead, created_by = request.user, pk=pk)

#     return render(request, 'lead/leads_detail.html', {
#         'lead': lead
#     })

# @login_required
# def leads_delete(request, pk):
#     lead = get_object_or_404(Lead, created_by = request.user, pk=pk)
#     lead.delete()

#     messages.success(request, "The lead was deleted.")

#     return redirect('leads:list')

# @login_required
# def leads_edit(request, pk):
#     lead = get_object_or_404(Lead, created_by = request.user, pk=pk)

#     if request.method == 'POST':
#         form = AddLeadForm(request.POST, instance=lead)

#         if form.is_valid():
#             form.save()

#             messages.success(request, 'The changes was saved.')

#             return redirect('leads:list')
#     else:
#         form = AddLeadForm(instance=lead)
        
#     return render(request, 'lead/leads_edit.html', {
#         'form': form
#     })

# @login_required
# def add_lead(request):
#     team = Team.objects.filter(created_by=request.user)[0]

#     if request.method == 'POST':
#         form = AddLeadForm(request.POST)

#         if form.is_valid():
#             # team = Team.objects.filter(created_by=request.user)[0]
#             lead = form.save(commit=False)
#             lead.created_by = request.user
#             lead.team = team
#             lead.save()

#             messages.success(request, "The lead was created.")

#             return redirect('leads:list')
#     else:
#         form = AddLeadForm()

#     return render(request, 'lead/add_lead.html', {
#         'form': form,
#         'team': team
#     })


class ConvertToClientView(LoginRequiredMixin, View):
    def get(self, request, *arg, **kwargs):
        pk = kwargs.get('pk')
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]

        client = Client.objects.create(
            name = lead.name,
            email = lead.email,
            description = lead.description,
            created_by = request.user,
            team = team,
        )

        lead.converted_to_client = True
        lead.save()

        

        # Convert lead comments to client comments

        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client = client,
                team = team,
                created_by = comment.created_by,
                content = comment.content
            )

        # Show message and redirect
        lead.delete()
        messages.success(request, "The lead was converted to a client.")

        return redirect('leads:list')

# @login_required
# def convert_to_client(request, pk):
#     lead = get_object_or_404(Lead, created_by = request.user, pk=pk)
#     team = Team.objects.filter(created_by=request.user)[0]

#     client = Client.objects.create(
#         name = lead.name,
#         email = lead.email,
#         description = lead.description,
#         created_by = request.user,
#         team = team,
#     )

#     lead.converted_to_client = True
#     lead.save()

#     messages.success(request, "The lead was converted to a client.")

#     return redirect('leads:list')

