# Generated by Django 5.1.6 on 2025-03-15 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_listings_category_alter_comments_datetime_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 14, 58, 2, 116426),
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Electronics", "Electronics"),
                    ("Fashion", "Fashion"),
                    ("Home", "Home"),
                    ("Study", "Study"),
                    ("Toys", "Toys"),
                ],
                max_length=18,
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 14, 58, 2, 115722),
            ),
        ),
    ]
