from django.db import models
import uuid


class Customers(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )

    chat_id = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    image = models.ImageField(upload_to="customers_images/")
    card_number = models.CharField(max_length=16)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    application_number = models.CharField(max_length=11, unique=True, default=uuid.uuid4().hex[:11])
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']
