# Generated by Django 3.0.6 on 2020-07-11 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='tips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='userdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(default='national institute of technology karnataka', max_length=100)),
                ('profileimg', models.ImageField(default='profileimg/me.jpg', upload_to='profileimg/')),
                ('totalsubmission', models.IntegerField(default=0)),
                ('correctsubmission', models.IntegerField(default=0)),
                ('ratting', models.IntegerField(default=1000)),
                ('score', models.IntegerField(default=0)),
                ('post', models.CharField(choices=[('s', 'student'), ('t', 'teacher')], default='s', max_length=2)),
                ('verified', models.CharField(choices=[('v', 'verified'), ('u', 'unverified')], default='u', max_length=2)),
                ('contribution', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='messagedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('seenstatus', models.CharField(default='unseen', max_length=6)),
                ('content', models.CharField(max_length=250)),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userdetails')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='usershashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.hashtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'hashtag')},
            },
        ),
    ]
