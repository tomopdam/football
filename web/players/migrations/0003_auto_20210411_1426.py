# Generated by Django 3.2 on 2021-04-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_rename_players_player'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='club',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='group',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='player',
            name='id_ext',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='nationality',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='player',
            name='overall',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='photo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='player',
            name='release_clause',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='wage',
            field=models.IntegerField(),
        ),
    ]
