from django.db.models import Q

from concurrent.futures import ThreadPoolExecutor
from celery import shared_task

from .exceptions import MailinglistTimeOutException
from .models import MailingList, Client, Message
from .utils import send_message, CircuitBreaker


@shared_task
def start_mailinglist(pk: int):
    '''
    Задача заускает рассылку
    '''
    mailinglist = MailingList.objects.filter(pk=pk).first()
    if mailinglist:
        messages = list()
        clients = Client.objects.filter(
            Q(tag=mailinglist.client_filter) | Q(code=mailinglist.client_filter)
        )
        with ThreadPoolExecutor() as pool:
            data = [
                {
                    'client_phone': client.phone,
                    'text': mailinglist.text,
                    'client_pk': client.pk,
                    'mailinglist_pk': mailinglist.pk,
                    'dttm_end': mailinglist.dttm_end,
                    'timeout': 0.5
                }
                for client in clients
            ]
            circuit_breaker = CircuitBreaker(
                callback=send_message,
                max_fail=3,
                reset_interval=5.0,
                time_window=0.1
            )
            results = pool.map(circuit_breaker.request, data)
            for result in results:
                if isinstance(result, MailinglistTimeOutException):
                    break
                elif isinstance(result, Message):
                    messages.append(result)

        Message.objects.bulk_create(messages)