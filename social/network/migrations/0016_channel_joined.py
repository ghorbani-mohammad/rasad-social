# Generated by Django 4.0.2 on 2022-02-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_alter_keyword_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='joined',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
