from PIL import Image
import torch
from torch import nn
from torchvision import transforms, models 

trained_model = None
class_names = ['Front Breakage', 'Front Crushed', 'Front Normal','Rear Breakage', 'Rear Crushed','Rear Normal']
# load the pre-trained ResNet50 model
class CarClassifierResNet(nn.Module):
  def __init__(self,num_classes=6):
    super().__init__()
    self.model = models.resnet50(weights = 'DEFAULT')

    # Freeze all layers except the final fully connected layer
    for param in self.model.parameters():
      param.requires_grad =  False
    
    # unfreeze layer4 and fc layer
    for param in self.model.layer4.parameters():
      param.requires_grad  =True

    # replace the final fully connected layer
    self.model.fc = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(self.model.fc.in_features, num_classes)
    )

  def forward(self,x):
    x = self.model(x)
    return x


def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_tensor = transform(image).unsqueeze_(0)

    global trained_model

    if trained_model is None:
        # Load the pre-trained model if it hasn't been loaded yet
        trained_model = CarClassifierResNet()
        trained_model.load_state_dict(torch.load('model/saved_model.pth'), map_location=torch.device('cpu'))
        trained_model.eval()

    with torch.no_grad():
        output = trained_model(image_tensor)
        _, predicted = torch.max(output.data, 1)
        return class_names[predicted.item()]
