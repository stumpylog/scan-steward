from django.db import models
from django.dispatch import receiver

from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import Pet
from scansteward.models import RoughDate
from scansteward.models import RoughLocation


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


# On change
@receiver(models.signals.post_save, sender=Pet)
@receiver(models.signals.post_save, sender=Person)
@receiver(models.signals.post_save, sender=RoughLocation)
@receiver(models.signals.post_save, sender=RoughDate)
# On delete
@receiver(models.signals.pre_delete, sender=Pet)
@receiver(models.signals.pre_delete, sender=Person)
@receiver(models.signals.pre_delete, sender=RoughLocation)
@receiver(models.signals.pre_delete, sender=RoughDate)
def mark_images_as_dirty_on_fk_change(
    sender: type[Pet | Person | RoughLocation | RoughDate],
    instance: Pet | Person | RoughLocation | RoughDate,
    *args,
    **kwargs,
):
    sender.objects.filter(people__id=instance.pk).update(is_dirty=True)
