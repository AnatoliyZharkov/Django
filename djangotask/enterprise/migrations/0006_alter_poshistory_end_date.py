# Generated by Django 3.2.9 on 2021-11-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_rename_pos_salary_positions_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poshistory',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
