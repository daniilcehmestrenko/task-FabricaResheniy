import requests
from requests.exceptions import Timeout
from django.conf import settings
from rest_framework import status

def send_message(text: str, phone: int, pk: int) -> bool:
    URL_SEND_API = settings.URL_SEND_API
    HEADERS = {
        "Authorization": "Bearer " + settings.TOKEN
    }
    status_message = None
    message = {
        "id": pk,
        "phone": phone,
        "text": text
    }
    try:
        response = requests.post(
            url=f'{URL_SEND_API}/send/{pk}',
            headers=HEADERS,
            json=message,
            timeout=1
        )
    except Timeout:
        return False

    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        status_message = data.get('message')

    return status_message == settings.SUCCESS_SEND