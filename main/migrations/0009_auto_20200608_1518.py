# Generated by Django 2.2.12 on 2020-06-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_crawlrequest_obey_robots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlrequest',
            name='tor_password',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
