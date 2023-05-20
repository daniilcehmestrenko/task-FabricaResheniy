from django.db.models import Q

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

        Message.objects.bulk_create(messages)