# Generated by Django 4.0.6 on 2022-08-11 01:39

from django.db import migrations
import utils.django.managers


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifySubmission',
            fields=[
            ],
            options={
                'verbose_name': 'verify submission',
                'verbose_name_plural': 'verify submissions',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('submissions.submission',),
            managers=[
                ('objects', utils.django.managers.BaseManager()),
            ],
        ),
    ]
