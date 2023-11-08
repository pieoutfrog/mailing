from django import forms

from mailing.models import MailingSettings, MailingMessage


class MailingSettingsCreateForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
        }


class MailingMessageCreateForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'
