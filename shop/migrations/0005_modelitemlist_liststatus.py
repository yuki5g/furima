# Generated by Django 2.1.7 on 2022-02-24 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_modelliststatus_modelshipstatus_modeltransactionlist_modeltransactionstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelitemlist',
            name='listStatus',
            field=models.ForeignKey(default=0, max_length=1, on_delete=django.db.models.deletion.CASCADE, to='shop.ModelListStatus', verbose_name='出品状態'),
        ),
    ]