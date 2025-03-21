# Generated by Django 5.1.7 on 2025-03-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_budjet', '0004_alter_customers_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customers',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='customers',
            name='application_number',
            field=models.CharField(default='a4634cb4e7a', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='card_number',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='customers',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='customers',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('rejected', 'Rejected'), ('accepted', 'Accepted')], default='new', max_length=10),
        ),
    ]
