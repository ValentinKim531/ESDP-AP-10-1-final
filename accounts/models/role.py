from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms.fields import MultipleChoiceField


class _MultipleChoiceField(MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.pop("base_field", None)
        kwargs.pop("max_length", None)
        super().__init__(*args, **kwargs)


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": _MultipleChoiceField,
                                    "choices": self.base_field.choices,
                                    **kwargs})


class Role(models.Model):
    PRIVILEGES_CHOICES = (
        ('ALLOW_ROLE_READ', "Привилегия на просмотр ролей"),
        ('ALLOW_ROLE_CREATE', "Привилегия на создание ролей"),
        ('ALLOW_ROLE_UPDATE', "Привилегия на обновление данных ролей"),
        ('ALLOW_ROLE_DELETE', "Привилегия на удаление ролей"),
        ('ALLOW_USER_ROLE_UPDATE', "Привилегия на обновление роли пользователя"),
        ('RESIDENT_PRIVILEGE', "Привилегия Резидента"),
        ('ALLOW_EVENT_CREATE', "Привилегия на создание мероприятия"),
        ('ALLOW_EVENT_UPDATE', "Привилегия на обновление данных мероприятия"),
        ('ALLOW_EVENT_DELETE', "Привилегия на удаление мероприятия"),
        ('ALLOW_NEWS_CREATE', "Привилегия на создание новости"),
        ('ALLOW_NEWS_UPDATE', "Привилегия на обновление данных новости"),
        ('ALLOW_NEWS_DELETE', "Привилегия на удаление новости"),
        ('ALLOW_REQUEST_CREATE', "Привилегия на создание запроса"),
        ('ALLOW_REQUEST_UPDATE', "Привилегия на обновление данных запроса"),
        ('ALLOW_REQUEST_DELETE', "Привилегия на удаление запроса"),
        ('ALLOW_REQUEST_FROM_ALL_RESIDENT_READ', "Привилегия на просмотр всех запросов"),
        ('ALLOW_REQUEST_WRITE_RESPONSE', "Привилегия на написание ответа запросу"),
        ('ALLOW_RESIDENT_BOOKED_READ', "Привилегия на просмотр, забранированных на мероприятие, резидентов"),
        ('ALLOW_RESIDENT_BOOKING', "Привилегия на удовлетворение брони резидента"),
        ('ALLOW_VOTE_CREATE', "Привилегия на создание голосования"),
        ('ALLOW_RESIDENT_UPDATE', "Привилегия на обновление данных резидента"),
        ('ALLOW_CHAT_CREATE', "Привилегия на создание чата"),
        ('ALLOW_CHAT_UPDATE', "Привилегия на обновление данных чата"),
    )
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Роль"
    )
    privileges = ChoiceArrayField(
        models.CharField(max_length=100, blank=True, choices=PRIVILEGES_CHOICES),
        default=list,
        blank=True,
        verbose_name="Привилегии"
    )

    def __str__(self):
        return self.name
