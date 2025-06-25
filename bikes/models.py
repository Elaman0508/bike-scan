from django.db import models


class BikePhoto(models.Model):
    image = models.ImageField(upload_to='bike_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    predicted_type = models.CharField(max_length=255, blank=True, null=True)
    estimated_price = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"BikePhoto {self.id} - {self.predicted_type}"
