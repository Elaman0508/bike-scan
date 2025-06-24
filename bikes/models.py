from django.db import models

class BikePhoto(models.Model):
    image = models.ImageField(upload_to='bike_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bike photo {self.id}"
