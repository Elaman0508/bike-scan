from django.urls import path
from .views import BikePricePredictionView, upload_bike_photo

urlpatterns = [
    path('predict/', BikePricePredictionView.as_view(), name='bike-predict'),
    path('upload/', upload_bike_photo, name='bike-upload'),
]
