# bikes/predictor.py
import torch
from torchvision import models, transforms
from PIL import Image
import os

# 📁 Загрузка классов
CLASSES_PATH = os.path.join(os.path.dirname(__file__), 'model/classes.txt')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/bike_classifier.pth')

with open(CLASSES_PATH) as f:
    classes = [line.strip() for line in f.readlines()]

# 🧠 Загружаем модель
model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# 🔄 Преобразования
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return classes[predicted[0]]
