# task-FabricaResheniy
# Инструкция для запуска

1. Создайте файл `.env` в корне проекта

Пример:

`DEBUG=1`

`SECRET_KEY= Secret Key`

`DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] 0.0.0.0`

`SQL_ENGINE=django.db.backends.postgresql`

`SQL_DATABASE=service`

`SQL_USER=user`

`SQL_PASSWORD=user`

`SQL_HOST=db`

`SQL_PORT=5432`

`CELERY_BROKER=redis://redis:6379/0`

`CELERY_BACKEND=redis://redis:6379/0`

`SUCCESS_SEND='OK'`

`URL_SEND_API='https://probe.fbrq.cloud/v1'`

`TOKEN='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE0MjIyMTYsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IktpbWNoaWRldmVsb3BlciJ9.R5mncjM_tjcfZmFmm9qnQpLocod9ANkbJ-UXHOkqLfM'`

2. Введите команду `docker-compose up`

3. Все готово, введите `0.0.0.0:8000` в адресной строке браузера

Для тестов добавлены тестовые данные, но рассылку нужно добавить вручную.

## Дополнительные задания:

 1. Написаны тесты
 2. Автодокументирование можно открыть по `0.0.0.0:8000/docs`
 3. Добавлены транзакции
 4. Отправка запросов на удаленное апи сделано через `ThreadPoolExecutor`
 5. Добавлен прерыватель
