# Generated by Django 5.1 on 2024-09-29 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('fileID', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('book_title', models.CharField(default=None, max_length=40)),
                ('book_photo', models.FileField(default=None, upload_to='books_photos/')),
                ('book_pdf', models.FileField(default=None, upload_to='books_pdf/')),
                ('bookDescription', models.TextField()),
                ('author', models.CharField(max_length=40)),
                ('publish', models.DateTimeField()),
                ('category', models.CharField(max_length=30)),
                ('avg_rating', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryUser',
            fields=[
                ('userid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=40)),
                ('photo', models.FileField(default='Media/default_image.jpeg', upload_to='profile_pic/')),
            ],
        ),
        migrations.CreateModel(
            name='FavouritiesBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pustakalay_app.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pustakalay_app.libraryuser')),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pustakalay_app.libraryuser'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0)),
                ('feedback', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pustakalay_app.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pustakalay_app.libraryuser')),
            ],
        ),
    ]
