from django.db import models
from treebeard.mp_tree import MP_Node

from scansteward.models import SimpleNamedModel
from scansteward.models import TimestampMixin


class Subject(SimpleNamedModel, TimestampMixin, MP_Node):
    """
    Holds the information about a Subject, roughly a tag
    """

    node_order_by = ["name"]


class Location(SimpleNamedModel, TimestampMixin, MP_Node):
    """
    Holds the information about a Location, some rough idea of a location, not actual GPS
    """

    node_order_by = ["name"]


class Person(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a single person
    """
