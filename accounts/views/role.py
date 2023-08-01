from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from accounts.models import Role, Account
from accounts.forms import RoleForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model


class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html'
    context_object_name = 'roles'


class RoleDetailView(DetailView):
    model = Role
    template_name = 'role_detail.html'
    context_object_name = 'role'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(role=self.object)
        context['privileges_list'] = self.object.PRIVILEGES_CHOICES
        return context


class RoleCreateView(CreateView):
    template_name = 'role_create.html'
    model = Role
    form_class = RoleForm

    def get_success_url(self):
        return reverse('role_detail', kwargs={'pk': self.object.pk})


class RoleUpdateView(UpdateView):
    template_name = 'role_update.html'
    model = Role
    form_class = RoleForm

    def get_success_url(self):
        return reverse('role_detail', kwargs={'pk': self.object.pk})


class RoleDeleteView(DeleteView):
    template_name = 'role_delete.html'
    model = Role
    success_url = reverse_lazy('role_list')
    context_object_name = 'role'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privileges_list'] = self.object.PRIVILEGES_CHOICES
        return context


class RoleTransferView(TemplateView):
    def get(self, request, *args, **kwargs):
        account_transfer_role = get_object_or_404(get_user_model(), pk=kwargs.get("pk"))
        account_transfer_role.role = get_object_or_404(Role, pk=request.GET.get('role_transfer_id'))
        account_transfer_role.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
