from django.urls import path
from mailing.views import MailingSettingsListView, MailingSettingsUpdateView, MailingSettingsDeleteView, \
    MailingSettingsCreateView, MailingSettingsDetailView, HomeView, MessageCreateView

app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/settings/view/', MailingSettingsListView.as_view(), name='mailing_list'),
    path('mailing/settings/<int:pk>/edit/', MailingSettingsUpdateView.as_view(), name='mailing_settings_update'),
    path('mailing/settings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='mailing_settings_delete'),
    path('mailing/settings/create/', MailingSettingsCreateView.as_view(), name='mailing_settings_create'),
    path('mailing/settings/<int:pk>/', MailingSettingsDetailView.as_view(), name='mailing_details'),
    path('mailing/message/view/', MessageCreateView.as_view(), name='message_create'),
]
