# Generated by Django 2.1 on 2019-07-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmodel',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]