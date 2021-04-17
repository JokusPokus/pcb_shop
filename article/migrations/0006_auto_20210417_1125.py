# Generated by Django 3.1.6 on 2021-04-17 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_offeredboardoptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='offeredboardoptions',
            options={'ordering': ['-created']},
        ),
        migrations.CreateModel(
            name='ExternalBoardOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attribute_options', models.JSONField()),
                ('external_shop', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='article.externalshop')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
