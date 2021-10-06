from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # What tag is applied to what item
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # We need 2 attributes. We don't just import the class so
    # we are not dependent on that class
    # Type of objects Type, ID
    # using content type we can create generic relationships
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
