from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimensions for the image are 70x70. You uploaded: {img.size}"
                )
 
            
def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    allowed_ext = [".jpg", ".jpeg", ".gif", ".png"]

    if ext not in allowed_ext:
        raise ValidationError("Unsupported file extension.")