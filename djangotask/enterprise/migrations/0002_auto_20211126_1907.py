# Generated by Django 3.2.9 on 2021-11-26 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positions',
            name='salary',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='worker',
            name='salary',
            field=models.FloatField(default=0),
        ),
    ]
