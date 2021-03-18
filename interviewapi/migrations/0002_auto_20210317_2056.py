# Generated by Django 2.2 on 2021-03-17 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interviewapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answeroption',
            old_name='option',
            new_name='option_answer',
        ),
        migrations.AddField(
            model_name='answertext',
            name='text_answer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='answertext',
            name='answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='interviewapi.Answer'),
        ),
        migrations.AlterField(
            model_name='option',
            name='options',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
