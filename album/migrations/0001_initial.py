<<<<<<< HEAD
# Generated by Django 4.2.11 on 2024-05-02 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.AutoField(primary_key=True, serialize=False)),
                ('album_name', models.CharField(max_length=50)),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('photo_data', models.BinaryField()),
                ('caption', models.CharField(max_length=50)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.album')),
=======
# Generated by Django 5.0.4 on 2024-05-01 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                ("album_id", models.AutoField(primary_key=True, serialize=False)),
                ("album_name", models.CharField(max_length=50)),
                ("date_of_creation", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                ("photo_id", models.AutoField(primary_key=True, serialize=False)),
                ("photo_data", models.BinaryField()),
                ("caption", models.CharField(max_length=50)),
                (
                    "album_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="album.album"
                    ),
                ),
>>>>>>> 1f0cb3d9d26e5b2bf9a89a3cffd8f0cda2d1b4a5
            ],
        ),
    ]