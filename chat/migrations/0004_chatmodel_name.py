# Generated by Django 2.1 on 2019-07-10 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_messagemodel_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]