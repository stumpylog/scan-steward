from django.db import models
from django.dispatch import receiver

from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import Pet
from scansteward.models import RoughDate
from scansteward.models import RoughLocation


@receiver(models.signals.post_delete, sender=Image)
def cleanup_files_on_delete(sender, instance: Image, using, **kwargs):
    """
    Removes files associated with the image when it is deleted.
    """
    if instance.full_size_path.exists():
        instance.full_size_path.unlink()
    if instance.thumbnail_path.exists():
        instance.thumbnail_path.unlink()
    if instance.original_path.exists():
        instance.original_path.unlink()


@receiver(models.signals.m2m_changed, sender=Image.tags.through)
@receiver(models.signals.m2m_changed, sender=Image.people.through)
@receiver(models.signals.m2m_changed, sender=Image.pets.through)
@receiver(models.signals.post_save, sender=Image)
def mark_image_as_dirty(sender, instance: Image, **kwargs):
    """
    Mark the image as dirty, ie, requiring a metadata sync to the file
    """

    # Use update so this doesn't loop
    Image.objects.filter(pk=instance.pk).update(is_dirty=True)


# On change
@receiver(models.signals.post_save, sender=Pet)
@receiver(models.signals.post_save, sender=Person)
# On delete
@receiver(models.signals.pre_delete, sender=Pet)
@receiver(models.signals.pre_delete, sender=Person)
def mark_images_as_dirty_on_m2m_change(
    sender: type[Pet | Person],
    instance: Pet | Person,
    *args,
    **kwargs,
):
    """
    Mark the image as dirty, ie, requiring a metadata sync to the file when various m2m relationships are changed
    """

    if isinstance(instance, Person):
        Image.objects.filter(people__pk=instance.pk).update(is_dirty=True)
    elif isinstance(instance, Pet):
        Image.objects.filter(pets__pk=instance.pk).update(is_dirty=True)


# On change
@receiver(models.signals.post_save, sender=RoughLocation)
@receiver(models.signals.post_save, sender=RoughDate)
# On delete
@receiver(models.signals.pre_delete, sender=RoughLocation)
@receiver(models.signals.pre_delete, sender=RoughDate)
def mark_images_as_dirty_on_fk_change(
    sender: type[RoughLocation | RoughDate],
    instance: RoughLocation | RoughDate,
    *args,
    **kwargs,
):
    """
    Mark the image as dirty, ie, requiring a metadata sync to the file when various foreign key relationships are changed
    """
    instance.images.all().update(is_dirty=True)
