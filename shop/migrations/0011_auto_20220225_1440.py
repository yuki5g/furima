# Generated by Django 2.1.7 on 2022-02-25 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_modelitemlist_transactionid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeltransactionlist',
            name='buyerId',
        ),
        migrations.RemoveField(
            model_name='modeltransactionlist',
            name='itemId',
        ),
        migrations.RemoveField(
            model_name='modeltransactionlist',
            name='sellerId',
        ),
        migrations.RemoveField(
            model_name='modeltransactionlist',
            name='shipStatus',
        ),
        migrations.RemoveField(
            model_name='modeltransactionlist',
            name='transactionStatus',
        ),
        migrations.DeleteModel(
            name='ModelTransactionList',
        ),
    ]