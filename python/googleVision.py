from google.cloud import vision
from google.cloud.vision import types
import os
import json

def OCR(img_url):
  try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/config/google api key.json'
    image = types.Image()
    image.source.image_uri = img_url
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    return response.text_annotations[0].description
  except Exception as e:
    return str(e)