from django.urls import path
from .views import BikePricePredictionView

urlpatterns = [
    path('predict/', BikePricePredictionView.as_view(), name='predict-bike'),
]
