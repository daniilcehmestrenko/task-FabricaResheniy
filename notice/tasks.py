from django.db.models import Q
from django.utils import timezone

from celery import shared_task

from .models import MailingList, Client, Message
from .service import send_message


@shared_task
def start_mailinglist(pk: int):
    mailinglist = MailingList.objects.filter(pk=pk).first()
    if mailinglist:
        messages = list()
        clients = Client.objects.filter(
            Q(tag=mailinglist.client_filter) | Q(code=mailinglist.client_filter)
        )
        for client in clients:
            if timezone.now() < mailinglist.dttm_end:
                status = send_message(
                    phone=client.phone,
                    text=mailinglist.text,
                    pk=client.pk
                )
                messages.append(Message(
                    status=status,
                    mailinglist_id=mailinglist.pk,
                    client_id=client.pk
                ))
        Message.objects.bulk_create(messages)