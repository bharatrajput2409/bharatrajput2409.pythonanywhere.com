# Generated by Django 3.0.6 on 2020-07-11 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='editorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('q_type', models.CharField(choices=[('objective', 'objective'), ('subjective', 'subjective')], default='objective', max_length=15)),
                ('total_submission', models.IntegerField(default=0)),
                ('correct_submission', models.IntegerField(default=0)),
                ('difficulty_level', models.CharField(choices=[('1', 'level 1'), ('2', 'level 2'), ('3', 'level 3')], default=1, max_length=2)),
                ('option1', models.CharField(max_length=150)),
                ('option2', models.CharField(max_length=150)),
                ('option3', models.CharField(max_length=150)),
                ('option4', models.CharField(max_length=150)),
                ('correct_ans', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='questiontag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=2)),
                ('status', models.BooleanField()),
                ('datetime', models.DateTimeField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('total_question', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='practice.quiz', verbose_name='quiz id'),
        ),
        migrations.CreateModel(
            name='editorial_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('editorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.editorial')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='editorial',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.question'),
        ),
        migrations.CreateModel(
            name='tag_in_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.question')),
                ('topic_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.questiontag')),
            ],
            options={
                'unique_together': {('question', 'topic_tag')},
            },
        ),
    ]
