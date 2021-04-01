# Generated by Django 3.1.6 on 2021-04-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210316_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='additional_line',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='house_number',
            field=models.CharField(default='9999', max_length=8),
        ),
        migrations.AddField(
            model_name='address',
            name='receiver_first_name',
            field=models.CharField(default='Max', max_length=30),
        ),
        migrations.AddField(
            model_name='address',
            name='receiver_last_name',
            field=models.CharField(default='Mustermann', max_length=40),
        ),
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(default='Musterstraße', max_length=40),
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='99999', max_length=5),
        ),
    ]
