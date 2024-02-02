from django.db import models


class TimestampMixin(models.Model):
    """
    Mixin class to provide created_at and updated_at columns in UTC
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleNamedModel(models.Model):
    """
    Basic model which provides a short name column and longer description column
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)

    description = models.CharField(max_length=1024, null=True, default=None, db_index=True)

    class Meta:
        abstract = True
