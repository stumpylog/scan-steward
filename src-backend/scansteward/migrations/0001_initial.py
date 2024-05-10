# Generated by Django 5.0.4 on 2024-04-11 14:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, db_index=True, default=None, max_length=1024, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Image",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "original_checksum",
                    models.CharField(
                        db_index=True,
                        help_text="The BLAKE3 checksum of the original file",
                        max_length=64,
                        unique=True,
                        verbose_name="blake3 hex digest",
                    ),
                ),
                (
                    "thumbnail_checksum",
                    models.CharField(
                        db_index=True,
                        help_text="The BLAKE3 checksum of the image thumbnail",
                        max_length=64,
                        unique=True,
                        verbose_name="blake3 hex digest",
                    ),
                ),
                (
                    "full_size_checksum",
                    models.CharField(
                        db_index=True,
                        help_text="The BLAKE3 checksum of the full size image",
                        max_length=64,
                        unique=True,
                        verbose_name="blake3 hex digest",
                    ),
                ),
                (
                    "phash",
                    models.CharField(
                        db_index=True,
                        help_text="The pHash (average) of the original file",
                        max_length=32,
                        verbose_name="perceptual average hash of the image",
                    ),
                ),
                (
                    "file_size",
                    models.PositiveBigIntegerField(
                        help_text="Size of the original file in bytes",
                        verbose_name="file size in bytes",
                    ),
                ),
                (
                    "orientation",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Horizontal"),
                            (2, "Mirror Horizontal"),
                            (3, "Rotate 180"),
                            (4, "Mirror Vertical"),
                            (5, "Mirror Horizontal And Rotate 270 Cw"),
                            (6, "Rotate 90 Cw"),
                            (7, "Mirror Horizontal And Rotate 90 Cw"),
                            (8, "Rotate 270 Cw"),
                        ],
                        default=1,
                        help_text="MWG Orientation flag",
                    ),
                ),
                ("description", models.TextField(blank=True, help_text="MWG Description tag", null=True)),
                (
                    "original",
                    models.CharField(max_length=1024, unique=True, verbose_name="Path to the original image"),
                ),
                (
                    "is_dirty",
                    models.BooleanField(
                        default=False,
                        help_text="The metadata is dirty and needs to be synced to the file",
                    ),
                ),
                (
                    "in_trash",
                    models.BooleanField(
                        default=False,
                        help_text="The image is in the trash and needs to be deleted from the file system on scheduled run",
                    ),
                ),
                ("is_starred", models.BooleanField(default=False, help_text="The image has been starred")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ImageSource",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default=None,
                        help_text="A description of this source, rendered as markdown",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, db_index=True, default=None, max_length=1024, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Pet",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, db_index=True, default=None, max_length=1024, null=True),
                ),
                (
                    "pet_type",
                    models.CharField(
                        blank=True,
                        choices=[("cat", "Cat"), ("dog", "Dog"), ("horse", "Horse")],
                        help_text="The type of pet this is",
                        max_length=10,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RoughDate",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("date", models.DateField(help_text="The date of the image, maybe not exact", unique=True)),
                (
                    "month_valid",
                    models.BooleanField(default=False, help_text="Is the month of this date valid?"),
                ),
                ("day_valid", models.BooleanField(default=False, help_text="Is the day of this date valid?")),
            ],
            options={
                "ordering": ["date"],
            },
        ),
        migrations.CreateModel(
            name="RoughLocation",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "country_code",
                    models.CharField(
                        db_index=True,
                        help_text="Country code in ISO 3166-1 alpha 2 format",
                        max_length=4,
                    ),
                ),
                (
                    "subdivision_code",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text="State, province or subdivision ISO 3166-2 alpha 2 format",
                        max_length=12,
                        null=True,
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text="City or town",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "sub_location",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text="Detailed location within a city or Town",
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ["country_code", "subdivision_code", "city", "sub_location"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, db_index=True, default=None, max_length=1024, null=True),
                ),
                ("applied", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="ImageInAlbum",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "sort_order",
                    models.PositiveBigIntegerField(verbose_name="Order of this image in the album"),
                ),
                (
                    "album",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scansteward.album",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="scansteward.image"),
                ),
            ],
            options={
                "ordering": ["sort_order"],
            },
        ),
        migrations.AddField(
            model_name="album",
            name="images",
            field=models.ManyToManyField(
                related_name="albums",
                through="scansteward.ImageInAlbum",
                to="scansteward.image",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="source",
            field=models.ForeignKey(
                blank=True,
                help_text="Source of the original image (box, deck, carousel, etc)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="scansteward.imagesource",
            ),
        ),
        migrations.CreateModel(
            name="PersonInImage",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "center_x",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "center_y",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "height",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "width",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "exclude_from_training",
                    models.BooleanField(
                        default=False,
                        help_text="For future growth, do not use this box for facial recognition training",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        help_text="A Thing is in this Image at the given location",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scansteward.image",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        help_text="Person is in this Image at the given location",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="images",
                        to="scansteward.person",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="image",
            name="people",
            field=models.ManyToManyField(
                help_text="These people are in the image",
                through="scansteward.PersonInImage",
                to="scansteward.person",
            ),
        ),
        migrations.CreateModel(
            name="PetInImage",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "center_x",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "center_y",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "height",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "width",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        help_text="A Thing is in this Image at the given location",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scansteward.image",
                    ),
                ),
                (
                    "pet",
                    models.ForeignKey(
                        help_text="Pet is in this Image at the given location",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="images",
                        to="scansteward.pet",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="image",
            name="pets",
            field=models.ManyToManyField(
                help_text="These pets are in the image",
                through="scansteward.PetInImage",
                to="scansteward.pet",
            ),
        ),
        migrations.AddConstraint(
            model_name="roughdate",
            constraint=models.UniqueConstraint(
                fields=("date", "month_valid", "day_valid"),
                name="unique-date",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="date",
            field=models.ForeignKey(
                blank=True,
                help_text="RoughDate when the image was taken, with as much refinement as possible",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="scansteward.roughdate",
            ),
        ),
        migrations.AddConstraint(
            model_name="roughlocation",
            constraint=models.UniqueConstraint(
                fields=("country_code", "subdivision_code", "city", "sub_location"),
                name="unique-location",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="location",
            field=models.ForeignKey(
                blank=True,
                help_text="Location where the image was taken, with as much refinement as possible",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="scansteward.roughlocation",
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="scansteward.tag",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="tags",
            field=models.ManyToManyField(
                help_text="These tags apply to the image",
                related_name="images",
                to="scansteward.tag",
            ),
        ),
        migrations.AddConstraint(
            model_name="imageinalbum",
            constraint=models.UniqueConstraint(fields=("sort_order", "album"), name="sorting-to-album"),
        ),
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(fields=("name", "parent"), name="name-to-parent"),
        ),
    ]
