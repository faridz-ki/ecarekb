# Generated by Django 3.2.5 on 2021-08-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210727_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterdata',
            name='density',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='masterdata',
            name='ghg',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='portiondata',
            name='mass',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='referencedata',
            name='ghg',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='referencedata',
            name='land_use',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='referencedata',
            name='water_use',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='farm',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='feed',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='land_use_change',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='month',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='packaging',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='processing',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='retail',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='seasonalitydata',
            name='transport',
            field=models.FloatField(),
        ),
    ]
