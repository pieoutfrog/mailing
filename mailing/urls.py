from django.urls import path
from mailing.views import MailingSettingsListView, MailingSettingsUpdateView, MailingSettingsDeleteView, \
    MailingSettingsCreateView, MailingSettingsDetailView, HomeView, MessageCreateView, UserListView, \
    MailingListManagerView, MessageListView, MessageDetailsView, MessageDeleteView, MessageUpdateView, ClientCreateView, \
    ClientDetailsView, ClientDeleteView, ClientUpdateView, ClientListView

app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/settings/view/', MailingSettingsListView.as_view(), name='mailing_list'),
    path('mailing/settings/<int:pk>/edit/', MailingSettingsUpdateView.as_view(), name='mailing_settings_update'),
    path('mailing/settings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='mailing_settings_delete'),
    path('mailing/settings/create/', MailingSettingsCreateView.as_view(), name='mailing_settings_create'),
    path('mailing/settings/<int:pk>/', MailingSettingsDetailView.as_view(), name='mailing_details'),
    path('mailing/message/view/', MessageCreateView.as_view(), name='message_create'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('mailing/settings/view/manage/', MailingListManagerView.as_view(), name='mailing_list_manager'),
    path('mailing/message/view/list/', MessageListView.as_view(), name='message_list'),
    path('mailing/message/view/<int:pk>/', MessageDetailsView.as_view(), name='message_details'),
    path('mailing/message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_update'),
    path('mailing/client/view/', ClientCreateView.as_view(), name='client_create'),
    path('mailing/client/view/list/', ClientListView.as_view(), name='client_list'),
    path('mailing/client/view/<int:pk>/', ClientDetailsView.as_view(), name='client_details'),
    path('mailing/client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing/client/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),

]
