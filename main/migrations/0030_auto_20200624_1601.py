# Generated by Django 3.0.7 on 2020-06-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_crawlrequest_link_extractor_allow_extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlrequest',
            name='formatable_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='http_status_response',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='invert_http_status',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='invert_text_match',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='param',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='post_dictionary',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='templated_url_type',
            field=models.CharField(choices=[('none', 'None'), ('get', 'GET'), ('post', 'POST')], default='none', max_length=15),
        ),
        migrations.AddField(
            model_name='crawlrequest',
            name='text_match_response',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
