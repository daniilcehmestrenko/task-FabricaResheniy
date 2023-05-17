from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers
from django.utils import timezone

from .tasks import start_mailinglist
from .models import MailingList, Client

class MailingListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        mailinglist: MailingList = super().create(validated_data)

        if timezone.now() > mailinglist.dttm_start:
            start_mailinglist.delay(mailinglist.pk)
        else:
            self.create_delay_task(mailinglist.pk)

        return mailinglist

    def create_delay_task(self, mailinglist_pk: int):
        mailinglist = MailingList.objects.get(pk=mailinglist_pk)

        crontab = CrontabSchedule.objects.create(
            minute=mailinglist.dttm_start.strftime('%M'),
            hour=mailinglist.dttm_start.strftime('%H'),
            day_of_month=mailinglist.dttm_start.strftime('%d'),
            month_of_year=mailinglist.dttm_start.strftime('%m'),
        )
        PeriodicTask.objects.create(
            crontab=crontab,
            name=f'Mailinglist {mailinglist.pk}',
            task='notice.tasks.start_mailinglist',
            one_off=True,
            args=[mailinglist.pk],
            start_time=mailinglist.dttm_start
        )

    class Meta:
        model = MailingList
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'