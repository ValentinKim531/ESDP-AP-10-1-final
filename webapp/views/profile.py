from django.db.models import Q
from django.http import JsonResponse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, UpdateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import json
from accounts.models import Account, Role
from accounts.cookie_auth import CookieJWTAuthentication
from webapp.forms import SearchForm


class ProfileListView(ListView):
    model = Account
    template_name = 'profile_list_django.html'
    context_object_name = 'accounts'
    authentication_classes = [CookieJWTAuthentication, ]
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        authenticator = self.authentication_classes[0]()
        try:
            user_auth_tuple = authenticator.authenticate(request)
        except AuthenticationFailed:
            return HttpResponseRedirect(reverse('login'))
        else:
            if user_auth_tuple:
                request.user, request.auth = user_auth_tuple
            else:
                return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        user_account = self.request.user
        queryset = super().get_queryset().exclude(pk=user_account.pk)
        queryset = queryset.order_by('-pk')
        queryset = [user_account] + list(queryset)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class ProfileDetailView(DetailView):
    model = Account
    template_name = 'profile_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_list'] = Role.objects.all()
        return context


def json_accounts(request, *args, **kwargs):
    if request.method == 'GET':
        search = request.GET.get('search')
        accounts = Account.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)) if search else Account.objects.all()
        return JsonResponse(list(accounts.values(*('id', 'occupation', 'first_name', 'last_name', 'avatar__image'))),
                            safe=False)
    if request.method == 'POST' and request.body:
        account = json.loads(request.body)
        try:
            account = Account.objects.create(**account)
            response = JsonResponse(account.as_dict)
            response.status_code = 201
        except Exception:
            response_data = {'detail': 'Некорректный набор данных'}
            response = JsonResponse(response_data)
            response.status_code = 400
        return response


class AccountUpdateView(UpdateView):
    model = Account
    template_name = 'profile_edit.html'
    fields = ['first_name', 'last_name', 'cities', 'occupation', 'phone', 'hobby', 'facts_about_me',
              'goal_for_the_year']
    success_url = reverse_lazy('account_detail')

    def get_success_url(self):
        return reverse_lazy('account_detail', kwargs={'pk': self.object.pk})
