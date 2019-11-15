from services.imageReader import readURL, readb64
from services.ocr import ocr
from services.faceComparision import compareFaces

def main(IdCardImage, SelfieImage, registerInfo):
  try:
    idCardImage = readb64(IdCardImage)
    selfieImage = readb64(SelfieImage)

    facialResponse = compareFaces(idCardImage, selfieImage)

    ocrResponse = ocr(idCardImage, registerInfo)

    return {
      'OCRInformation': ocrResponse['info'],
      'OCRResult': ocrResponse['verify'],
      'Face': facialResponse
    }
  except Exception as e:
    return str(e)