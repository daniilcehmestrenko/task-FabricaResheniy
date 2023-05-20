from django.db.models import Count, Q, F

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet

from .serializers import (
    MailingListSerializer,
    MailingListStatDetailSerializer,
    MailingListStatSerializer,
    ClientSerializer,
)
from .models import MailingList, Client
from .service import MailingListService


class MailingListViewSet(ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        service = MailingListService(serializer.data.get('id'))
        service.start_or_delay()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingListStatViewSet(ViewSet):
    def retrieve(self, request: Request, pk: int):
        queryset = (
            MailingList.objects.filter(pk=pk)
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
        )
        serializer = MailingListStatDetailSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request: Request):
        queryset = (
            MailingList.objects.values('messages__status')
                .annotate(
                    count_message=Count('messages'),
                    status_message=F('messages__status')
                )
                .values()
        )
        count_mailinglist = MailingList.objects.all().count()
        serializer = MailingListStatSerializer(queryset, many=True)

        data = {
            "mailinglist_stats": serializer.data,
            "count_mailinglist": count_mailinglist
        }

        return Response(data, status=status.HTTP_200_OK)
