# Generated by Django 3.1.4 on 2021-06-13 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20210614_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation_request',
            name='image',
        ),
        migrations.AlterField(
            model_name='customer',
            name='random_image_number',
            field=models.CharField(default='66685', max_length=7),
        ),
    ]