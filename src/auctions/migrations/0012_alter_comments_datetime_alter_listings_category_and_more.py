# Generated by Django 5.1.6 on 2025-03-15 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_alter_comments_datetime_alter_listings_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 22, 39, 53, 696981),
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="category",
            field=models.CharField(
                choices=[("Electronics", "Electronics")], max_length=18
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 22, 39, 53, 696291),
            ),
        ),
    ]
