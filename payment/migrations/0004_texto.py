# Generated by Django 4.2.7 on 2023-11-19 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_cobranca'),
    ]

    operations = [
        migrations.CreateModel(
            name='Texto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=1000)),
            ],
        ),
    ]
