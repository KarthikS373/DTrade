# Generated by Django 4.0.6 on 2022-08-01 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='futureshistory',
            name='orderDetails',
        ),
        migrations.RemoveField(
            model_name='futuresorders',
            name='usr',
        ),
        migrations.RemoveField(
            model_name='spotorders',
            name='usr',
        ),
        migrations.DeleteModel(
            name='visitor',
        ),
        migrations.DeleteModel(
            name='FuturesHistory',
        ),
        migrations.DeleteModel(
            name='FuturesOrders',
        ),
        migrations.DeleteModel(
            name='SpotOrders',
        ),
    ]