# Generated by Django 2.1.7 on 2022-02-24 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20220224_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelitemlist',
            name='transactionId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ModelTransactionList', verbose_name='取引情報'),
        ),
    ]
