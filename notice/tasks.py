from django.db.models import Q
from django.utils import timezone
from django.db import transaction

from concurrent.futures import ThreadPoolExecutor
from celery import shared_task

from .models import MailingList, Client, Message
from .utils import send_message


@shared_task
def start_mailinglist(pk: int):
    mailinglist = MailingList.objects.filter(pk=pk).first()
    if mailinglist:
        messages = list()
        clients = Client.objects.filter(
            Q(tag=mailinglist.client_filter) | Q(code=mailinglist.client_filter)
        )
        with ThreadPoolExecutor() as pool:
            data = [
                {
                    'phone': client.phone,
                    'text': mailinglist.text,
                    'id': client.pk,
                    'mailinglist_pk': mailinglist.pk,
                    'dttm_end': mailinglist.dttm_end
                }
                for client in clients
            ]
            results = pool.map(send_message, data)

            for result in results:
                if result:
                    messages.append(result)

        # for client in clients:
        #     if timezone.now() < mailinglist.dttm_end:
        #         status = send_message(
        #             phone=client.phone,
        #             text=mailinglist.text,
        #             pk=client.pk
        #         )
        #         messages.append(Message(
        #             status=status,
        #             mailinglist_id=mailinglist.pk,
        #             client_id=client.pk
        #         ))
        #     else:
        #         break

        with transaction.atomic():
            Message.objects.bulk_create(messages)