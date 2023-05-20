import requests
from requests.exceptions import Timeout
from django.conf import settings
from django.utils import timezone
from rest_framework import status

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
    try:
        if timezone.now() < dttm_end:
            response = requests.post(
                url=f'{URL_SEND_API}/send/{data.get("id")}',
                headers=HEADERS,
                json=json,
                timeout=1
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
                raise Timeout
        else:
            raise Timeout
    except Timeout:
        return None