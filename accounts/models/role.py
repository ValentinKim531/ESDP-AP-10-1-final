from django.db import models


class Role(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        verbose_name="Роль"
    )
    privileges = models.ManyToManyField(
        'Privileges',
        verbose_name="Привилегии"
    )

    def __str__(self):
        return self.name
