from accounts.models import Account
from chat.models import ChatRoom
from django import forms


class GroupChatForm(forms.ModelForm):
    class UserChoiceField(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.get_full_name() or obj.email

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['users'].queryset = Account.objects.exclude(id=user.id)
            self.fields['users'].label = 'Выберите пользователей'
        self.fields['name'].label = False
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название чата'
        self.fields['name'].widget.attrs['class'] = 'chat_name_field'
        self.fields['description'].label = False
        self.fields['description'].widget.attrs['placeholder'] = 'Описание чата'
        self.fields['description'].widget.attrs['class'] = 'chat_description_field'
        self.fields['avatar'].widget.attrs['class'] = 'chat_avatar_label'
        self.fields['avatar'].label = False

    users = UserChoiceField(
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'avatar', 'users']


class ChannelForm(forms.ModelForm):
    users = GroupChatForm.UserChoiceField(
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['users'].queryset = Account.objects.exclude(id=user.id)
            self.fields['users'].label = 'Выберите пользователей'
        self.fields['name'].label = False
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название канала'
        self.fields['name'].widget.attrs['class'] = 'channel_name_field'
        self.fields['description'].label = False
        self.fields['description'].widget.attrs['placeholder'] = 'Описание канала'
        self.fields['description'].widget.attrs['class'] = 'channel_description_field'
        self.fields['avatar'].widget.attrs['class'] = 'channel_avatar_label'
        self.fields['avatar'].label = False

    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'avatar', 'users']
