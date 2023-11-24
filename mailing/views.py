from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import BlogPost, Category
from config import settings
from mailing.forms import MailingSettingsCreateForm, MailingMessageCreateForm, ClientCreateForm
from mailing.models import MailingSettings, MailingMessage, Client
from users.models import User


class HomeView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Количество рассылок всего
        if settings.CACHE_ENABLED:
            total_mailings = cache.get('total_mailings')
            if total_mailings is None:
                total_mailings = MailingSettings.objects.count()
                cache.set('total_mailings', total_mailings)
        else:
            total_mailings = MailingSettings.objects.count()

        context['total_mailings'] = total_mailings

        # Количество активных рассылок
        active_mailings = MailingSettings.objects.filter(is_active=True).count()
        context['active_mailings'] = active_mailings

        # Количество уникальных клиентов для рассылок
        unique_clients = Client.objects.distinct().count()
        context['unique_clients'] = unique_clients

        # 3 случайные статьи из блога
        random_articles = BlogPost.objects.order_by('?')[:3]
        context['random_articles'] = random_articles

        categories = Category.objects.all()
        context['categories'] = categories

        if settings.CACHE_ENABLED:
            top_article = cache.get('top_article')
            if top_article is None:
                top_article = BlogPost.objects.order_by('-views_count').first()
                cache.set('top_article', top_article)
        else:
            top_article = BlogPost.objects.order_by('-views_count').first()

        context['top_article'] = top_article


        if settings.CACHE_ENABLED:
            latest_article = cache.get('latest_article')
            if latest_article is None:
                latest_article = BlogPost.objects.order_by('-created_date').first()
                cache.set('latest_article', latest_article)
        else:
            latest_article = BlogPost.objects.order_by('-created_date').first()

        context['latest_article'] = latest_article

        return context


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'mailing/user_list.html'
    context_object_name = 'user_list'

    def test_func(self):
        return self.request.user.groups.filter(name='Менеджер').exists()

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False)
        return queryset

    def post(self, request):
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_blocked = not user.is_blocked
        user.save()
        return self.get(request)


class MailingListManagerView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list_manager.html'
    context_object_name = 'mailing_clients'

    def test_func(self):
        return self.request.user.groups.filter(name='Менеджер').exists()

    def post(self, request):
        mailing_id = request.POST.get('mailing_id')  # Получаем идентификатор рассылки из запроса
        mailing = MailingSettings.objects.get(id=mailing_id)  # Получаем объект рассылки по идентификатору

        if mailing.is_active is True:
            mailing.status = 'running'
        else:
            mailing.status = 'created'

        mailing.is_active = not mailing.is_active
        mailing.save()
        return redirect('mailing:mailing_list_manager')


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailing_clients'
    mailing_settings = MailingSettings.objects.all()
    context = {
        'mailing_settings': mailing_settings,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mailing/mailing_settings_create.html'
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']  # Получаем объект MailingMessage из формы
        # в функции по крону будет создаваться лог
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mailing/mailing_details.html'
    model = MailingSettings
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mailing/mailing_settings_create.html'
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']
        mailing_settings = form.save(commit=False)
        mailing_settings.message = mailing_message
        mailing_settings.save()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('mailing:mailing_details', args=[self.kwargs.get('pk')])


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mailing/mailingclient_confirm_delete.html'
    model = MailingSettings

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageCreateForm
    template_name = 'mailing/message_create.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailing:home')


class MessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage
    template_name = 'mailing/message_list.html'
    context_object_name = 'mailing_messages'
    mailing_messages = MailingMessage.objects.all()
    context = {
        'mailing_messages': mailing_messages,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'mailing/message_details.html'
    model = MailingMessage
    context_object_name = 'mailing_messages'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mailing/message_confirm_delete.html'
    model = MailingMessage

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mailing/message_create.html'
    model = MailingMessage
    form_class = MailingMessageCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']
        mailing_settings = form.save(commit=False)
        mailing_settings.message = mailing_message
        mailing_settings.save()

        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('mailing:mailing_details', args=[self.kwargs.get('pk')])


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = 'mailing/client_create.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailing:home')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'mailing/client_details.html'
    model = Client
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mailing/client_confirm_delete.html'
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mailing/client_create.html'
    model = Client
    form_class = ClientCreateForm

    def form_valid(self, form):
        client = form.cleaned_data['client']
        mailing_settings = form.save(commit=False)
        mailing_settings.client = client
        mailing_settings.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('mailing:client_details', args=[self.kwargs.get('pk')])
