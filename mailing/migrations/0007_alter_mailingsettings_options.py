# Generated by Django 4.2.7 on 2023-11-20 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailingmessage_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingsettings',
            options={'permissions': [('can_set_mailing_activity', 'Can change mailing activity')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]