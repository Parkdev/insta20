# Generated by Django 3.0.7 on 2020-07-02 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20200702_0714'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followrelations',
            unique_together={('from_relation', 'to_relation', 'relation_type')},
        ),
    ]