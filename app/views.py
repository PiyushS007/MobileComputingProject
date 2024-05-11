from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64


@csrf_exempt
def preprocess_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Get the uploaded image
        uploaded_image = request.FILES['image']

        # Read the image into a PIL Image object
        pil_image = Image.open(uploaded_image)

        # Convert the image to black and white
        processed_image = pil_image.convert('L')

        # Convert the processed image to bytes
        with io.BytesIO() as image_buffer:
            processed_image.save(image_buffer, format='JPEG')
            encoded_string = base64.b64encode(image_buffer.getvalue()).decode()

        # Construct the data URI
        data_uri =encoded_string

        return JsonResponse({'processedImageURL': data_uri})
    else:
        return JsonResponse({'error': 'Image file not found'}, status=400)
