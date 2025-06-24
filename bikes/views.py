from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import BikePhoto
from .serializers import BikePhotoSerializer

class BikePricePredictionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = BikePhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Заглушка AI: распознаём тип велосипеда и цену
            predicted_type = "Fixie"
            predicted_price = "от 300 до 500 $"
            return Response({
                "status": "ok",
                "type": predicted_type,
                "estimated_price": predicted_price,
                "photo": serializer.data
            })
        return Response(serializer.errors, status=400)
