from django import forms
from webapp.models import Events, News, AdminRequest, ChatRequest, SubscriptionLevel, ListVotes, Vote, VotingOptions
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
            "name",
            "user",
            "cities",
            "description",
            "photo"
        )

        labels = {
            "name": "Наименование новости",
            "user": "Пользователь",
            "cities": "Город",
            "description": "Описание новости",
            "photo": "Фото",
        }

    def clean_title(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError(
                "Наименование должно быть длиннее 2 символов"
            )
        if News.objects.filter(name=name).exists():
            raise ValidationError(
                "Наименование с таким именем уже есть"
            )
        return name


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = (
            'name', 'cities', 'type_events', 'cities', 'events_at', 'sponsor', 'number_of_seats', 'start_register_at',
            'end_register_at', 'description', 'place', 'price', 'photo')
        labels = {
            "name": "Название",
            "cities": "Город",
            "type_events": "Тип мероприятия",
            "events_at": "Дата мероприятия",
            "sponsor": "Спонсор",
            "number_of_seats": "Количество мест",
            "start_register_at": "Начало регистрации",
            "end_register_at": "Конец регистрации",
            "description": "Описание",
            "place": "Место расположения",
            "price": "Цена",
            "photo": "Фото"
        }


class ChatRequestForm(forms.ModelForm):
    class Meta:
        model = ChatRequest
        fields = ("chat_name", "second_user", "cities", "description", "rules")
        labels = {
            "chat_name": "Наименование чата",
            "second_user": "Второй пользователь",
            "cities": "Город чата",
            "description": "Описание",
            "rules": "Правила чата",
        }

    def clean_chat_name(self):
        chat_name = self.cleaned_data.get('chat_name')
        if len(chat_name) < 3:
            raise ValidationError('Наименование чата не может состоять из 1 или 2 символов')
        return chat_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 3:
            raise ValidationError('Описание чата обязательное поле')
        return description

    def clean_rules(self):
        rules = self.cleaned_data.get('rules')
        if len(rules) < 3:
            raise ValidationError('Должны быть правила чата')
        return rules


class SubscriptionLevelForm(forms.ModelForm):
    class Meta:
        model = SubscriptionLevel
        fields = ("level_name", "price")
        labels = {
            "level_name": "Название подписки",
            "price": "Цена подписки",
        }


class AdminRequestSenderTextForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ("request_text",)
        labels = {
            "request_text": "Текст запроса"
        }


class AdminRequestSubLevelForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ("request_text", "sub_level")
        labels = {
            "request_text": "Текст запроса",
            "sub_level": "Уровень подписки"
        }


class AdminRequestReviewerForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ("approved", "response_text")
        labels = {
            "approved": "Утвержден?",
            "response_text": "Текст ответа"
        }

    def clean_response_text(self):
        response_text = self.cleaned_data.get('response_text')
        if len(response_text) < 3:
            raise ValidationError('Ответ на запрос должен состоять более чем из 3 символов обязательное поле')
        return response_text


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label="Поиск резидентов")


class ListVoteForm(forms.ModelForm):
    class Meta:
        model = ListVotes
        fields = (
            'name_of_the_vote', 'user_who_created_list_votes')
        labels = {
            "name_of_the_vote": "Название голосования",
            "user_who_created_list_votes": "Пользовать",
        }


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = (
            'question_to_vote',)
        labels = {
            "question_to_vote": "Вопрос на голосование",
        }


class VotingOptionsForm(forms.ModelForm):
    class Meta:
        model = VotingOptions
        fields = (
            'vote', 'option',)
        labels = {
            "vote": "Голосование",
            "option": "Вариант",
        }
