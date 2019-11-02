from google.cloud import vision
from google.cloud.vision import types
import os
import json
import cv2

def OCR(image):
  try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/config/google api key.json'
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.png', image)
    encoded_image = encoded_image.tobytes()
    image = vision.types.Image(content=encoded_image)
    response = client.document_text_detection(image=image)
    return response.text_annotations[0].description
  except Exception as e:
    return str(e)