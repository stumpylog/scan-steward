from django.db import models
from django.dispatch import receiver

from scansteward.models import Image
from scansteward.models import Location
from scansteward.models import Person
from scansteward.models import Pet


@receiver(models.signals.post_delete, sender=Image)
def cleanup_image_deletion(sender, instance, using, **kwargs):
    # TODO: Maybe delete the fullsize, etc?
    pass


@receiver(models.signals.m2m_changed, sender=Image.tags.through)
@receiver(models.signals.m2m_changed, sender=Image.people.through)
@receiver(models.signals.m2m_changed, sender=Image.pets.through)
@receiver(models.signals.post_save, sender=Image)
def mark_image_as_dirty(sender, instance: Image, **kwargs):
    # Mark the image as dirty, ie, requiring a metadata sync to the file
    # Use update so this doesn't loop
    Image.objects.filter(pk=instance.pk).update(is_dirty=False)


@receiver(models.signals.post_save, sender=Person)
def mark_person_images_as_dirty(sender, instance: Person, **kwargs):
    Image.objects.filter(people__id=instance.pk).update(is_dirty=True)


@receiver(models.signals.post_save, sender=Pet)
def mark_petimages_as_dirty(sender, instance: Pet, **kwargs):
    Image.objects.filter(pets__id=instance.pk).update(is_dirty=True)


@receiver(models.signals.post_save, sender=Location)
def mark_location_updates_as_dirty(sender, instance: Location, **kwargs):
    Image.objects.filter(location=instance).update(is_dirty=True)
