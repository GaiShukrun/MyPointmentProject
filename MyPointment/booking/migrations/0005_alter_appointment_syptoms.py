# Generated by Django 4.1.3 on 2022-12-16 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_appointment_syptoms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='syptoms',
            field=models.TextField(blank=True, null=True),
        ),
    ]
