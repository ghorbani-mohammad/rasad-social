# Generated by Django 4.0.2 on 2022-02-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_post_body_alter_post_network_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='share_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='views_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]