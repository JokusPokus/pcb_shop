# Generated by Django 3.1.6 on 2021-04-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210401_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='additional_line',
            new_name='address_extension',
        ),
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='address',
            name='receiver_first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='address',
            name='receiver_last_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=5),
        ),
    ]
