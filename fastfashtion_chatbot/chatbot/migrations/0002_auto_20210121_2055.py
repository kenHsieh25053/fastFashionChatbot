# Generated by Django 3.1.5 on 2021-01-21 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermodel',
            old_name='email_address',
            new_name='email',
        ),
        migrations.RemoveField(
            model_name='emailmodel',
            name='email',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='line_channel_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]