from django import forms
from accounts.models import Role
from django.core.exceptions import ValidationError


class RoleForm(forms.ModelForm):
    privileges = forms.MultipleChoiceField(choices=Role.PRIVILEGES_CHOICES, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Role
        fields = ("name", "privileges")
        labels = {
            "name": "Название роли",
            "privileges": "Привилегии"
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError(
                "Наименование роли должно быть длиннее 2 символов"
            )
        return name
