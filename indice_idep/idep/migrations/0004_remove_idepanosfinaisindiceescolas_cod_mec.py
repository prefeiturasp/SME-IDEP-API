# Generated by Django 2.2.1 on 2019-06-07 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('idep', '0003_idepanosfinaisindiceescolas_idepanosfinaismetasescolas_idepanosfinaisparametrosescolas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idepanosfinaisindiceescolas',
            name='cod_mec',
        ),
    ]
