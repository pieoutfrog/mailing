from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from mailing.forms import MailingSettingsCreateForm, MailingMessageCreateForm
from mailing.models import MailingSettings, MailingMessage


class HomeView(TemplateView):
    template_name = 'mailing/index.html'


class MailingSettingsListView(ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailing_clients'
    mailing_settings = MailingSettings.objects.all()
    context = {
        'mailing_settings': mailing_settings,
    }


class MailingSettingsCreateView(CreateView):
    template_name = 'mailing/mailing_settings_create.html'
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']  # Получаем объект MailingMessage из формы
        # в функции по крону будет создаваться лог

        return super().form_valid(form)

    # проверка времени в кроне
    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')


class MailingSettingsDetailView(DetailView):
    template_name = 'mailing/mailing_details.html'
    model = MailingSettings
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнительный код для получения дополнительных данных, если требуется
        return context


class MailingSettingsUpdateView(UpdateView):
    template_name = 'mailing/mailing_settings_create.html'
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']
        mailing_settings = form.save(commit=False)
        mailing_settings.message = mailing_message
        mailing_settings.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing_details', args=[self.kwargs.get('pk')])


class MailingSettingsDeleteView(DeleteView):
    template_name = 'mailing/mailingclient_confirm_delete.html'
    model = MailingSettings

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageCreateForm
    template_name = 'mailing/message_create.html'

    def get_success_url(self):
        return reverse_lazy('mailing:home')
