# Generated by Django 4.1.10 on 2023-08-02 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signup_with_mongo', '0002_signup_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='signup_data',
        ),
    ]