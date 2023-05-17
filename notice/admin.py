from django.contrib import admin

from .models import MailingList, Client, Message


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('dttm_start', 'text', 'client_filter', 'dttm_end')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'tag', 'timezone')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('dttm_created', 'status', 'mailinglist', 'client')