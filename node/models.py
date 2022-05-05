from django.db import models

import uuid

# Create your models here.


class Node(models.Model):
    """
    Node Model
    """

    # Basic Information
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pre_name = models.CharField(max_length=10)
    display_name = models.CharField(max_length=10)
    domain_name = models.CharField(max_length=100)

    # Port Settings
    default_port_start = models.IntegerField()
    default_port_end = models.IntegerField()

    # Management Settings
    manage_password = models.CharField(max_length=16)

    # More Details
    status = models.CharField(max_length=50, default='Offline')
    announcement = models.TextField(blank=True)
    max_bandwidth = models.IntegerField()
    price = models.IntegerField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.display_name
