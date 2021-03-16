# Generated by Django 3.1.6 on 2021-03-16 11:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('articleCategoryID', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('gerberFileName', models.CharField(max_length=100)),
                ('gerberHash', models.CharField(max_length=100)),
                ('dimensionX', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('dimensionY', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('differentDesigns', models.PositiveIntegerField()),
                ('layers', models.PositiveIntegerField()),
                ('deliveryFormat', models.CharField(max_length=30)),
                ('thickness', models.FloatField()),
                ('color', models.CharField(max_length=30)),
                ('surfaceFinish', models.CharField(max_length=30)),
                ('copperWeight', models.PositiveIntegerField()),
                ('goldFingers', models.CharField(max_length=30)),
                ('castellatedHoles', models.CharField(max_length=30)),
                ('removeOrderNum', models.CharField(max_length=30)),
                ('confirmProdFile', models.CharField(max_length=30)),
                ('flyingProbeTest', models.CharField(max_length=30)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='article.articlecategory'),
        ),
    ]
