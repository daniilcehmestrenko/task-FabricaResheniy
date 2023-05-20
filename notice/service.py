from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .tasks import start_mailinglist
from .models import MailingList


class MailingListService:
    def __init__(self, mailinglist_pk: int) -> None:
        self.mailinglist = self.__get_mailinglist(mailinglist_pk)

    def start_or_delay(self):
        if timezone.now() > self.mailinglist.dttm_start:
            start_mailinglist.delay(self.mailinglist.pk)
        else:
            self.__create_delay_task()

    def __get_mailinglist(self, pk: int) -> MailingList | None:
        return MailingList.objects.filter(pk=pk).first()

    def __create_delay_task(self) -> None:
        crontab = CrontabSchedule.objects.create(
            minute=self.mailinglist.dttm_start.strftime('%M'),
            hour=self.mailinglist.dttm_start.strftime('%H'),
            day_of_month=self.mailinglist.dttm_start.strftime('%d'),
            month_of_year=self.mailinglist.dttm_start.strftime('%m'),
        )
        PeriodicTask.objects.create(
            crontab=crontab,
            name=f'Mailinglist {self.mailinglist.pk}',
            task='notice.tasks.start_mailinglist',
            one_off=True,
            args=[self.mailinglist.pk],
            start_time=self.mailinglist.dttm_start
        )