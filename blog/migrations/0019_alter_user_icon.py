# Generated by Django 5.0.7 on 2024-07-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_user_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='default_icon.png', upload_to=''),
        ),
    ]
