from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BikePhotoSerializer
from .predictor import predict
from .utils import get_price_by_type, search_olx_bikes

from django.shortcuts import render
from .models import BikePhoto
from PIL import Image, UnidentifiedImageError


class BikePricePredictionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BikePhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save()
            image_path = photo.image.path

            try:
                predicted_label = predict(image_path)
                price_range = get_price_by_type(predicted_label)

                return Response({
                    "status": "ok",
                    "type": predicted_label,
                    "estimated_price": price_range,
                    "photo": serializer.data
                })

            except UnidentifiedImageError:
                return Response({"error": "Некорректное изображение"}, status=400)

        return Response(serializer.errors, status=400)


def upload_bike_photo(request):
    result = None
    similar_bikes = []

    if request.method == 'POST' and request.FILES.get('image'):
        try:
            photo = BikePhoto.objects.create(image=request.FILES['image'])
            predicted_label = predict(photo.image.path)
            price = get_price_by_type(predicted_label)

            photo.predicted_type = predicted_label
            photo.estimated_price = price
            photo.save()

            result = {
                "type": predicted_label,
                "estimated_price": price,
                "photo": photo,
            }

            similar_bikes = search_olx_bikes(predicted_label)

        except UnidentifiedImageError:
            result = {"error": "Загруженное изображение не распознано."}

    history = BikePhoto.objects.order_by('-uploaded_at')

    return render(request, 'bikes/upload.html', {
        'result': result,
        'history': history,
        'similar_bikes': similar_bikes,
    })
