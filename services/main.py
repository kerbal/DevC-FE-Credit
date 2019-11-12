from services.imageReader import readURL
from services.ocr import ocr
from services.faceComparision import compareFaces

def main(IdCardURL, SelfieURL):
  try:
    idCardImage = readURL(IdCardURL)
    selfieImage = readURL(SelfieURL)
    ocrResponse = ocr(idCardImage)
    facialResponse = compareFaces(idCardImage, selfieImage)
    return {
      'OCR': ocrResponse,
      'FacialCompare': facialResponse
    }
  except Exception as e:
    return str(e)