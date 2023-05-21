import requests
from requests.exceptions import Timeout

from django.conf import settings
from django.utils import timezone
from rest_framework import status

from typing import Callable

from .exceptions import (
    MailinglistTimeOutException,
    StatusResponseException,
    CircuitBreakerException
)
from .models import Message

def send_message(data: dict) -> Message | None:
    SUCCESS_SEND: str = settings.SUCCESS_SEND
    URL_SEND_API: str = settings.URL_SEND_API
    HEADERS: dict[str, str] = {"Authorization": "Bearer " + settings.TOKEN}

    dttm_end = data.get('dttm_end')
    json = {
        "id": data.get('id'),
        "phone": data.get('phone'),
        "text": data.get('text')
    }
    if timezone.now() < dttm_end:
        response = requests.post(
            url=f'{URL_SEND_API}/send/{data.get("id")}',
            headers=HEADERS,
            json=json,
            timeout=data.get('timeout')
        )
        if response.status_code == status.HTTP_200_OK:
            success_flag: str = response.json().get('message')
            status_answer = SUCCESS_SEND == success_flag                
            return Message(
                status=status_answer,
                mailinglist_id=data.get('mailinglist_pk'),
                client_id=data.get('id')
            )
        else:
            raise StatusResponseException
    else:
        raise MailinglistTimeOutException


class CircuitBreaker:
    def __init__(self, callback: Callable[[dict], Message | Exception],
                 time_window: float,
                 max_fail: int,
                 reset_interval: float) -> None:

        self.callback = callback # принимает функцию
        self.time_window = time_window # окно в котором можно фейлить запросы без счета ошибок
        self.max_fail = max_fail # максимальное количество ошибок
        self.reset_interval = reset_interval # время через которое цепь разомкнется
        self.last_request_time = None
        self.last_fail_time = None
        self.current_fail = 0

    def request(self, *args, **kwargs):
        if self.current_fail >= self.max_fail:
            if timezone.now() > self.last_request_time \
                    + timezone.timedelta(seconds=self.reset_interval):
                # произойдет сброс и цепь разомкнется, если интервала сброса прошло
                self.__reset()
                return self.__do_request(*args, **kwargs)
            else:
                return CircuitBreakerException()
        else:
            if self.last_fail_time and timezone.now() > self.last_fail_time \
                    + timezone.timedelta(seconds=self.time_window):
                # если запрос попадает в окно без подсчета ошибок, произойдет сброс
                self.__reset()
            return self.__do_request(*args, **kwargs)

    def __reset(self):
        '''
        Метод сбрасывает количество ошибок и время последнего запроса с ошибкой
        '''
        self.last_fail_time = None
        self.current_fail = 0

    def __do_request(self, *args, **kwargs):
        '''
        Метод вызывает callback, который будет рейзить исключение,
        которое мы обработаем и выполним логику добавления ошибок запросов
        '''
        try:
            self.last_request_time = timezone.now()
            return self.callback(*args, **kwargs)

        except Timeout:
            self.current_fail += 1
            if self.last_fail_time is None:
                self.last_fail_time = timezone.now()

            return Timeout()

        except MailinglistTimeOutException:
            return MailinglistTimeOutException()

        except StatusResponseException:
            self.current_fail += 1
            if self.last_fail_time is None:
                self.last_fail_time = timezone.now()

            return StatusResponseException()