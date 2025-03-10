# Generated by Django 5.1.6 on 2025-02-26 03:29

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailerMessage',
            fields=[
                ('id', models.AutoField(db_column='id', editable=False, help_text='Message identification number.', primary_key=True, serialize=False, verbose_name='Message ID')),
                ('status', models.PositiveIntegerField(choices=[(0, 'Sent'), (1, 'Failed'), (2, 'Queued'), (3, 'Canceled')], db_column='status', default=2, help_text='Status of the e-mail message.', verbose_name='Status')),
                ('from_email', models.EmailField(db_column='from_email', default='djmailer@gaw.sh', help_text='Sender ("From") e-mail address of the message.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='From E-mail Address')),
                ('from_name', models.CharField(blank=True, db_column='from_name', help_text='Sender name in the e-mail "From" address.', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='From Name')),
                ('reply_to_email', models.EmailField(db_column='reply_to_email', default='djmailer@gaw.sh', help_text='"Reply-To" e-mail address of the message.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Reply-To E-mail Address')),
                ('reply_to_name', models.CharField(blank=True, db_column='reply_to_name', help_text='Reply-To name of the message.', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='From Name')),
                ('to_email', models.EmailField(db_column='to_email', help_text='Primary ("To") recipient e-mail address of the message.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Recipient E-mail Address')),
                ('to_name', models.CharField(blank=True, db_column='to_name', help_text='Recipient name in the e-mail "To" address.', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Recipient Name')),
                ('subject', models.CharField(db_column='subject', help_text='Subject of the e-mail message.', max_length=32, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='E-mail Subject')),
                ('body', models.TextField(db_column='body', help_text='Body of the e-mail message.', verbose_name='E-mail Body')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', help_text='Date and time when the e-mail message was created.', verbose_name='Created At')),
                ('sent_at', models.DateTimeField(db_column='sent_at', default=None, editable=False, help_text='Date and time when the e-mail message was sent.', null=True, verbose_name='Sent At')),
            ],
            options={
                'verbose_name': 'Message',
                'db_table': 'messages',
                'ordering': ('-id',),
                'managed': True,
                'default_related_name': 'message',
            },
        ),
        migrations.CreateModel(
            name='MailerTemplate',
            fields=[
                ('id', models.AutoField(db_column='id', editable=False, help_text='Template identification number.', primary_key=True, serialize=False, verbose_name='Template ID')),
                ('active', models.BooleanField(db_column='active', default=True, help_text='Is the e-mail template active and available?', verbose_name='Active?')),
                ('name', models.CharField(db_column='name', help_text='Name of the e-mail template.', max_length=32, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Template Name')),
                ('description', models.TextField(blank=True, db_column='description', help_text='Description of the e-mail template.', verbose_name='Template Description')),
                ('from_email', models.EmailField(db_column='from_email', default='djmailer@gaw.sh', help_text='From address of e-mail message(s) sent using the template.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Sender E-mail Address')),
                ('from_name', models.CharField(blank=True, db_column='from_name', help_text='From name of e-mail message(s) sent using the template.', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='From Name')),
                ('reply_to_email', models.EmailField(db_column='reply_to_email', default='djmailer@gaw.sh', help_text='Reply-To e-mail address of message(s) sent using the template.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Reply-To E-mail Address')),
                ('reply_to_name', models.CharField(blank=True, db_column='reply_to_name', help_text='Reply-To e-mail name of message(s) sent using the template.', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Reply-To Name')),
                ('subject', models.CharField(db_column='subject', help_text='Subject of e-mail message(s) sent using the template.', max_length=32, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='E-mail Subject')),
                ('body', models.TextField(db_column='body', help_text='Body of e-mail message(s) sent using the template.', verbose_name='E-mail Body')),
            ],
            options={
                'verbose_name': 'Template',
                'db_table': 'templates',
                'ordering': ('name',),
                'managed': True,
                'default_related_name': 'template',
            },
        ),
        migrations.CreateModel(
            name='MailerVariable',
            fields=[
                ('name', models.SlugField(db_column='name', help_text='Name of the variable to be made available to all templates.', primary_key=True, serialize=False, verbose_name='Name')),
                ('value', models.TextField(db_column='value', help_text='Value of the global e-mail template variable.', verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Variable',
                'db_table': 'variables',
                'ordering': ('name',),
                'managed': True,
                'default_related_name': 'variable',
            },
        ),
        migrations.CreateModel(
            name='MailerRecipient',
            fields=[
                ('id', models.AutoField(db_column='id', editable=False, help_text='Recipient identification number.', primary_key=True, serialize=False, verbose_name='Recipient ID')),
                ('email', models.EmailField(db_column='email', help_text='Recipient address of a message.', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Recipient E-mail Address')),
                ('name', models.CharField(blank=True, db_column='name', default=None, help_text='Recipient Name', max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1), django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Recipient Name')),
                ('message', models.ForeignKey(db_column='message', help_text='Message related to the recipient.', on_delete=django.db.models.deletion.CASCADE, to='mailer.mailermessage', verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Recipient',
                'db_table': 'recipients',
                'ordering': ('-id',),
                'managed': True,
                'default_related_name': 'recipient',
                'unique_together': {('email', 'message')},
            },
        ),
    ]
