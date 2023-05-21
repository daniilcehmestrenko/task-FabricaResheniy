from django.utils import timezone
from django.db import transaction
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .tasks import start_mailinglist
from .models import MailingList


class MailingListService:
    def start(self, pk: int):
        mailinglist = self.__get_mailinglist(pk)

        if mailinglist:
            start_mailinglist.delay(pk)
            return True
        else:
            return False

    def start_or_delay(self, pk: int):
        mailinglist = self.__get_mailinglist(pk)

        if mailinglist:
            if timezone.now() > mailinglist.dttm_start:
                start_mailinglist.delay(mailinglist.pk)
            else:
                self.__create_delay_task(mailinglist)

    def __get_mailinglist(self, pk: int) -> MailingList | None:
        return MailingList.objects.filter(pk=pk).first()

    def __create_delay_task(self, mailinglist: MailingList) -> None:
        with transaction.atomic():
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