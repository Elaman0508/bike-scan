from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BikePhotoSerializer

import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import os
from django.shortcuts import render
from .models import BikePhoto


def predict_image_class(image_path):
    # Загружаем предобученную модель ResNet
    model = models.resnet18(pretrained=True)
    model.eval()

    # Преобразования для входного изображения
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])

    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # добавляем размерность для batch

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    # Загрузка классов ImageNet
    labels_path = os.path.join(os.path.dirname(__file__), 'imagenet_classes.txt')
    if not os.path.exists(labels_path):
        import urllib.request
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",
            labels_path
        )

    with open(labels_path) as f:
        classes = [line.strip() for line in f.readlines()]

    return classes[predicted[0]]


class BikePricePredictionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BikePhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save()
            image_path = photo.image.path

            # Получение предсказания от модели
            predicted_label = predict_image_class(image_path)

            # Упрощённая логика оценки стоимости
            if "bike" in predicted_label.lower():
                price_range = "от 300 до 500 $"
            else:
                price_range = "неизвестно"

            return Response({
                "status": "ok",
                "type": predicted_label,
                "estimated_price": price_range,
                "photo": serializer.data
            })

        return Response(serializer.errors, status=400)



def upload_bike_photo(request):
    result = None

    if request.method == 'POST' and request.FILES.get('image'):
        photo = BikePhoto.objects.create(image=request.FILES['image'])
        predicted_label = predict_image_class(photo.image.path)
        if "bike" in predicted_label.lower():
            price = "от 300 до 500 $"
        else:
            price = "неизвестно"

        result = {
            "type": predicted_label,
            "estimated_price": price,
            "photo": photo,
        }

    return render(request, 'bikes/upload.html', {'result': result})