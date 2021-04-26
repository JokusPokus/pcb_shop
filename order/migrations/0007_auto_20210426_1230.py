# Generated by Django 3.1.6 on 2021-04-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_shippingmethod_shipping_provider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='value',
            new_name='amount',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article2order',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='shippingmethod',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]