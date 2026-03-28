# From develop merge: restaurant fields, threaded reviews, opening hours

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_alter_category_options_alter_menuitem_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="restaurant_photos/"
            ),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="price_range",
            field=models.CharField(
                choices=[("1", "€"), ("2", "€€"), ("3", "€€€")],
                default="2",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="restaurants.review",
            ),
        ),
        migrations.CreateModel(
            name="OpeningHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day",
                    models.IntegerField(
                        choices=[
                            (1, "Monday"),
                            (2, "Tuesday"),
                            (3, "Wednesday"),
                            (4, "Thursday"),
                            (5, "Friday"),
                            (6, "Saturday"),
                            (7, "Sunday"),
                        ]
                    ),
                ),
                ("open_time", models.TimeField()),
                ("close_time", models.TimeField()),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opening_hours",
                        to="restaurants.restaurant",
                    ),
                ),
            ],
            options={
                "ordering": ["day"],
                "unique_together": {("restaurant", "day")},
            },
        ),
    ]
