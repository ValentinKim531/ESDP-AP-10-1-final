from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import AdminRequest
from django.urls import reverse, reverse_lazy
from accounts.models import Account
from django.shortcuts import redirect
from webapp.forms import ChatRequestForm, SubscriptionLevelForm, AdminRequestSenderTextForm, AdminRequestSubLevelForm, \
    AdminRequestReviewerForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequestListView(ListView):
    model = AdminRequest
    template_name = 'request_list.html'
    context_object_name = 'requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requests = AdminRequest.objects.filter(is_deleted=False).order_by("-created_at")
        if self.request.user.role and 'ALLOW_REQUEST_FROM_ALL_RESIDENT_READ' in self.request.user.role.privileges:
            if self.request.GET.get("from_user"):
                if self.request.GET.get("from_user") == "me":
                    requests = requests.filter(user_sender=self.request.user)
                else:
                    try:
                        user_id = int(self.request.GET.get("from_user"))
                        requests = requests.filter(user_sender=Account.objects.get(id=user_id))
                    except:
                        requests = requests
        else:
            requests = requests.filter(user_sender=self.request.user)
        if self.request.GET.get("approved"):
            if self.request.GET.get("approved") == "true":
                requests = requests.filter(approved=True)
            elif self.request.GET.get("approved") == "false":
                requests = requests.filter(approved=False)
            elif self.request.GET.get("approved") == "none":
                requests = requests.filter(approved=None)
        if self.request.GET.get("filter") and self.request.GET.get("filter") in ['sub_level', 'chat_request',
                                                                                 'other_request']:
            if self.request.GET.get("filter") == 'other_request':
                requests = requests.filter(sub_level__isnull=True, chat_request__isnull=True)
            else:
                par = self.request.GET.get("filter") + "__isnull"
                requests = requests.filter(**{par: False})
        context['requests'] = requests
        return context


class AdminRequestDetailView(UserPassesTestMixin, DetailView):
    model = AdminRequest
    template_name = 'request_detail.html'
    context_object_name = 'request_detail'

    def test_func(self):
        return self.request.user.role and 'ALLOW_REQUEST_FROM_ALL_RESIDENT_READ' in self.request.user.role.privileges or get_object_or_404(AdminRequest, pk=self.kwargs['pk']).user_sender == self.request.user


class AdminRequestCreateView(CreateView):
    model = AdminRequest
    template_name = 'request_create.html'

    def get_context_data(self, **kwargs):
        context = {
            'form_chat': ChatRequestForm,
            'form_sub': AdminRequestSubLevelForm,
            'form_text': AdminRequestSenderTextForm,
            'type_form': 'def_request'
        }
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('chat_name'):
            form_chat_dict = {
                'chat_name': request.POST.get('chat_name'),
                'second_user': request.POST.get('second_user'),
                'cities': request.POST.get('cities'),
                'description': request.POST.get('description'),
                'rules': request.POST.get('rules')
            }
            form_text_dict = {
                'request_text': request.POST.get('request_text')
            }
            form_chat = ChatRequestForm(form_chat_dict)
            form_text = AdminRequestSenderTextForm(form_text_dict)
            if form_chat.is_valid() and form_text.is_valid():
                user_sender = request.user
                chat_request = form_chat.save(commit=False)
                chat_request.save()
                admin_request = AdminRequest.objects.create(user_sender=user_sender, chat_request=chat_request,
                                                            request_text=request.POST.get('request_text'))
                return redirect(reverse('request_detail', kwargs={'pk': admin_request.pk}))
            context = {
                'form_chat': form_chat,
                'form_sub': AdminRequestSubLevelForm,
                'form_text': form_text,
                'type_form': 'chat_request'
            }
            return self.render_to_response(context=context)
        elif request.POST.get('sub_level'):
            form_sub = AdminRequestSubLevelForm(request.POST)
            if form_sub.is_valid():
                sub_request = form_sub.save(commit=False)
                sub_request.user_sender = request.user
                sub_request.save()
                return redirect(reverse('request_detail', kwargs={'pk': sub_request.pk}))
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': form_sub,
                'form_text': AdminRequestSenderTextForm,
                'type_form': 'sub_request'
            }
            return self.render_to_response(context=context)
        else:
            form_text = AdminRequestSenderTextForm(request.POST)
            if form_text.is_valid():
                text_request = form_text.save(commit=False)
                text_request.user_sender = request.user
                text_request.save()
                return redirect(reverse('request_detail', kwargs={'pk': text_request.pk}))
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': AdminRequestSubLevelForm,
                'form_text': form_text,
                'type_form': 'def_request'
            }
            return self.render_to_response(context=context)


class AdminRequestUpdateView(UpdateView):
    model = AdminRequest
    template_name = 'request_update.html'

    def get_context_data(self, **kwargs):
        request_data = get_object_or_404(AdminRequest, pk=self.kwargs.get("pk"))
        if request_data.chat_request:
            context = {
                'form_chat': ChatRequestForm(request_data.chat_request.__dict__),
                'form_sub': AdminRequestSubLevelForm,
                'form_text': AdminRequestSenderTextForm,
                'type_form': 'chat_request'
            }
        elif request_data.sub_level:
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': AdminRequestSubLevelForm(request_data.__dict__),
                'form_text': AdminRequestSenderTextForm,
                'type_form': 'sub_request'
            }
        else:
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': AdminRequestSubLevelForm,
                'form_text': AdminRequestSenderTextForm(request_data.__dict__),
                'type_form': 'def_request'
            }
        context['request_detail'] = request_data
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('chat_name'):
            form_chat_dict = {
                'chat_name': request.POST.get('chat_name'),
                'second_user': request.POST.get('second_user'),
                'cities': request.POST.get('cities'),
                'description': request.POST.get('description'),
                'rules': request.POST.get('rules')
            }
            form_text_dict = {
                'request_text': request.POST.get('request_text')
            }
            form_chat = ChatRequestForm(form_chat_dict)
            form_text = AdminRequestSenderTextForm(form_text_dict)
            if form_chat.is_valid() and form_text.is_valid():
                chat_request = form_chat.save(commit=False)
                chat_request.save()
                admin_request = get_object_or_404(AdminRequest, pk=self.kwargs.get("pk"))
                admin_request.chat_request = chat_request
                admin_request.request_text = request.POST.get('request_text')
                admin_request.save()
                return redirect(reverse('request_detail', kwargs={'pk': admin_request.pk}))
            context = {
                'form_chat': form_chat,
                'form_sub': AdminRequestSubLevelForm,
                'form_text': form_text,
                'type_form': 'chat_request'
            }
            return self.render_to_response(context=context)
        elif request.POST.get('sub_level'):
            form_sub = AdminRequestSubLevelForm(request.POST)
            if form_sub.is_valid():
                sub_request = form_sub.save(commit=False)
                sub_request.user_sender = request.user
                sub_request.save()
                return redirect(reverse('request_detail', kwargs={'pk': sub_request.pk}))
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': form_sub,
                'form_text': AdminRequestSenderTextForm,
                'type_form': 'sub_request'
            }
            return self.render_to_response(context=context)
        else:
            form_text = AdminRequestSenderTextForm(request.POST)
            if form_text.is_valid():
                text_request = form_text.save(commit=False)
                text_request.user_sender = request.user
                text_request.save()
                return redirect(reverse('request_detail', kwargs={'pk': text_request.pk}))
            context = {
                'form_chat': ChatRequestForm,
                'form_sub': AdminRequestSubLevelForm,
                'form_text': form_text,
                'type_form': 'def_request'
            }
            return self.render_to_response(context=context)


class AdminRequestDeleteView(DeleteView):
    template_name = 'request_delete.html'
    model = AdminRequest
    context_object_name = 'request_detail'
    success_url = reverse_lazy('request_list')


class AdminResponseView(UpdateView):
    model = AdminRequest
    template_name = 'request_response.html'

    def get_context_data(self, **kwargs):
        context = {
            'request_detail': get_object_or_404(AdminRequest, pk=self.kwargs['pk']),
            'form': AdminRequestReviewerForm
        }
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            form = AdminRequestReviewerForm(request.POST)
            if form.is_valid():
                user_reviewer = request.user
                request_response = get_object_or_404(AdminRequest, pk=self.kwargs['pk'])
                request_response.response_text = request.POST.get('response_text')
                if request.POST.get('approved') == 'true':
                    request_response.approved = True
                elif request.POST.get('approved') == 'false':
                    request_response.approved = False
                else:
                    request_response.approved = None
                request_response.user_reviewer = user_reviewer
                request_response.closed_at = timezone.now()
                request_response.save()
                return redirect(reverse('request_detail', kwargs={'pk': request_response.pk}))
            context = {
                'request_detail': get_object_or_404(AdminRequest, pk=self.kwargs['pk']),
                'form': form
            }
            return self.render_to_response(context=context)
        context = {
            'request_detail': get_object_or_404(AdminRequest, pk=self.kwargs['pk']),
            'form': AdminRequestReviewerForm
        }
        return self.render_to_response(context=context)
