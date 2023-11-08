from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings, EmailLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message_content')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'frequency', 'start_time', 'end_time', 'status')
    list_filter = ('frequency', 'status')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('datetime_attempt', 'status', 'settings')