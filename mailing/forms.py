from django import forms

from mailing.models import MailingSettings, MailingMessage, Client


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
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.cleaned_data['owner']
        if commit:
            instance.save()
        return instance


class MailingMessageCreateForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.cleaned_data['owner']
        if commit:
            instance.save()
        return instance


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.cleaned_data['owner']
        if commit:
            instance.save()
        return instance
