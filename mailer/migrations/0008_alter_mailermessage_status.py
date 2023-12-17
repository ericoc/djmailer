# Generated by Django 5.0 on 2023-12-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0007_alter_mailermessage_recipient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailermessage',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Sent'), (1, 'Failed'), (2, 'Queued'), (3, 'Canceled')], db_column='status', default=2, help_text='Status of the e-mail message.', verbose_name='Message Status'),
        ),
    ]
