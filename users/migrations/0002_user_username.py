# Generated by Django 3.0.3 on 2020-05-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='Guest', max_length=20, null=True, verbose_name='username'),
        ),
    ]