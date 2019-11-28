import cv2
from google.cloud.vision import types
from google.cloud import vision
import os

def OCR(image, template = False):
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/config/google api key.json'
  client = vision.ImageAnnotatorClient()
  success, encoded_image = cv2.imencode('.png', image)
  encoded_image = encoded_image.tobytes()
  img = vision.types.Image(content=encoded_image)
  response = client.document_text_detection(image=img, image_context={"language_hints": ["vi"]})
  if template == False:
    print(response.text_annotations[0].description)
    return response.text_annotations[0].description
  else:
    return response.text_annotations