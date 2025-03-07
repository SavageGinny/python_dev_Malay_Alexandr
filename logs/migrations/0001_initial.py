# Generated by Django 5.1.6 on 2025-03-06 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'event_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('user_id', models.IntegerField()),
                ('space_id', models.IntegerField()),
            ],
            options={
                'db_table': 'logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpaceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'space_type',
                'managed': False,
            },
        ),
    ]
