# Generated by Django 4.1.10 on 2023-08-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_with_mongo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='signup_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('user_name', models.CharField(max_length=122)),
                ('email', models.CharField(max_length=122)),
                ('password', models.CharField(max_length=128)),
                ('access_token', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
