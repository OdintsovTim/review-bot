# Generated by Django 3.2.4 on 2021-06-22 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_webhooksecrettoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='is_opened',
        ),
        migrations.AddField(
            model_name='discussion',
            name='commit',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='discussions', to='review.commit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discussion',
            name='participants',
            field=models.ManyToManyField(to='review.Developer'),
        ),
    ]