# Generated by Django 3.2.5 on 2021-08-05 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210806_0041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referencedata',
            old_name='ghg',
            new_name='ghg_global',
        ),
        migrations.AddField(
            model_name='referencedata',
            name='ghg_retail',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
