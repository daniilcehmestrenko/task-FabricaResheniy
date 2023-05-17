from django.db.models import Count, F, Q

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet

from .serializers import MailingListSerializer, ClientSerializer
from .models import MailingList, Client

class MailingListViewSet(ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingListStatViewSet(ViewSet):
    def retrieve(self, request: Request, pk: int):
        data = (
            MailingList.objects.prefetch_related('messages')
                .filter(pk=pk)
                .annotate(
                    count_message=Count('messages'),
                    count_sent_messages=Count(
                        'messages',
                        filter=Q(messages__status=True)
                    ),
                    count_not_sent_messages=Count(
                        'messages',
                        filter=Q(messages__status=False)
                    )
                )
                .values(
                    pk=F('pk'),
                    message_text=F('text'),
                    start_date=F('dttm_start'),
                    end_date=F('dttm_end'),
                    filter=F('client_filter'),
                    count_all_message=F('count_message'),
                    count_sent_messages=F('count_sent_messages'),
                    count_not_sent_messages=F('count_not_sent_messages'),
                )
        )
        return Response(data)

    def list(self, request: Request):
        malinglist_stats = (
            MailingList.objects.prefetch_related('messages')
                .values('messages__status')
                .annotate(
                    count_message=Count('messages'),
                )
                .values(
                    pk=F('pk'),
                    mailing_text=F('text'),
                    count_mess=F('count_message'),
                    status_message=F('messages__status'),
                    client_filter=F('client_filter')
                )
        )
        count_mailinglist = MailingList.objects.all().count()
        data = {
            "mailinglist_stats": malinglist_stats,
            "count_mailinglist": count_mailinglist
        }
        return Response(data)