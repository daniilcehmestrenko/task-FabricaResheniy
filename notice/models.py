from django.db import models
from django.core.validators import RegexValidator


class MailingList(models.Model):
    dttm_start = models.DateTimeField()
    text = models.TextField()
    client_filter = models.CharField(
        db_index=True,
        max_length=50
    )
    dttm_end = models.DateTimeField()


class Client(models.Model):
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'7\d{10}')]
    )
    code = models.CharField(
        db_index=True,
        max_length=5
    )
    tag = models.CharField(
        db_index=True,
        max_length=20
    )
    timezone = models.CharField(
        max_length=50,
        help_text='Формат: UCT+01:00'
    )


class Message(models.Model):
    dttm_created = models.DateTimeField(
        auto_now_add=True
    )
    status = models.BooleanField()
    mailinglist = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages'
    )