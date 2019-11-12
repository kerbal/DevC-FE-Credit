import cv2
from google.cloud.vision import types
from google.cloud import vision
import os

def OCR(image):
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/config/google api key.json'
  client = vision.ImageAnnotatorClient()
  success, encoded_image = cv2.imencode('.png', image)
  encoded_image = encoded_image.tobytes()
  img = vision.types.Image(content=encoded_image)
  response = client.document_text_detection(image=img)
  return response.text_annotations[0].description