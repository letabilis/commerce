# Generated by Django 5.1.6 on 2025-03-15 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_category_alter_comments_datetime_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 22, 35, 15, 7660),
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="category",
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name="listings",
            name="datetime",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(2025, 3, 15, 22, 35, 15, 6968),
            ),
        ),
    ]
