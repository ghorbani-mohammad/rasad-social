# Generated by Django 4.0.2 on 2022-03-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_post_category_post_ner_post_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='ner',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='sentiment',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
