# Generated by Django 4.0.4 on 2022-07-05 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_move_find_defend_attack'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchia',
            name='life',
            field=models.IntegerField(default=50),
        ),
    ]