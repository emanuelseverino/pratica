# Generated by Django 4.2.7 on 2023-11-17 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='update_id',
            new_name='update_in',
        ),
    ]
