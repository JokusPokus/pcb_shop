# Generated by Django 3.1.6 on 2021-04-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20210426_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='paymentMethod',
            new_name='payment_method',
        ),
        migrations.RenameField(
            model_name='paymentmethod',
            old_name='name',
            new_name='provider_name',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='value',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='changed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]