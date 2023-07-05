import torch
from models.utils import test_transform, denormalize
from models.VGG16 import TransformerNet
from PIL import Image
from torch.autograd import Variable
from torchvision.utils import save_image


def style_transfer(image_path, output_path, transformer) -> None:
    transform = test_transform()

    # Prepare input
    image_tensor = Variable(transform(Image.open(image_path)))
    image_tensor = image_tensor.unsqueeze(0)

    # # Stylize image
    with torch.no_grad():
        stylized_image = denormalize(transformer(image_tensor)).cpu()

    # save stylized image
    save_image(stylized_image, output_path)

