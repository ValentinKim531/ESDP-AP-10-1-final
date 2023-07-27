from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse

from accounts.models import Account
from webapp.forms import VoteForm, VotingOptionsForm, ListVoteForm
from webapp.models import ListVotes, Vote, VotingOptions, UsersWhoVoted


class VoteCreateView(CreateView):
    template_name = 'vote_create.html'
    model = Vote
    form_class = VoteForm

    def get_success_url(self):
        return reverse('vote_list_create_view')


class VoteListCreateView(CreateView):
    template_name = 'vote_list_create.html'
    model = ListVotes
    form_class = ListVoteForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            vote_last = Vote.objects.all().last()
            vote_list = form.save(commit=False)
            form.save()
            vote_list.vote.add(vote_last)
            return redirect('/vote/option')
        context = {'form': form}
        return self.render_to_response(context)


class VoteOptionCreateView(CreateView):
    template_name = 'vote_option_create.html'
    model = VotingOptions
    form_class = VotingOptionsForm

    def get_success_url(self):
        return reverse('vote_option_create_view')


class VotelineView(ListView):
    model = Vote
    template_name = 'vote_list.html'
    context_object_name = 'vot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = ListVotes.objects.all()
        context['votes'] = vote
        return context


class VoteDetailView(DetailView):
    model = ListVotes
    template_name = 'vote_detail.html'
    context_object_name = 'vote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote_list = self.object
        for i in vote_list.vote.all():
            option = VotingOptions.objects.filter(vote=i.pk)
            all_user_who_voted = 0
            for j in option:
                all_user_who_voted += UsersWhoVoted.objects.filter(possible_answer=j).count()
            for j in option:
                voted_user = UsersWhoVoted.objects.filter(possible_answer=j).count()
                j.procent = int((voted_user / all_user_who_voted) * 100)
            context['votes'] = option
            context['vot'] = i.question_to_vote
        voted_user = UsersWhoVoted.objects.filter(users=self.request.user).last()
        context['voted_user'] = voted_user
        return context


class VoteBookedView(TemplateView):
    template_name = 'vote_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        vote_option = get_object_or_404(VotingOptions, pk=kwargs.get("pk"))
        UsersWhoVoted.objects.create(possible_answer=vote_option, users=user)
        return redirect('voteline')
