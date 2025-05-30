# Generated by Django 5.2 on 2025-04-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_category_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, to='store.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='store.size'),
        ),
    ]
