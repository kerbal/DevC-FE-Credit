from services.imageReader import readURL, readb64
from services.ocr import ocr
from services.faceComparision import compareFaces
import services.database as db

def main(IdCardImage, SelfieImage, registerInfo):
  try:
    idCardImage = readb64(IdCardImage)
    selfieImage = readb64(SelfieImage)

    face = compareFaces(idCardImage, selfieImage)
    ocrinfo, verify = ocr(idCardImage, registerInfo)

    # ocrinfo = {
    #   "Birthday": "04-09-1999",
    #   "District": "Tân An",
    #   "Fullname": "Huỳnh Lượng Phương Trúc",
    #   "Hometown": "Long An",
    #   "IdentityNumber": "301667360",
    #   "Province": "Long An"
    # }

    # verify = {
    #   "BirthdayResult": True,
    #   "DistrictResult": True,
    #   "FullnameResult": True,
    #   "HometownResult": True,
    #   "IdentityNumberResult": True,
    #   "OCRResult": True,
    #   "ProvinceResult": True
    # }

    userId = db.insertUser(registerInfo['PhoneNumber'])

    db.insertRegisterForm(
      userId,
      registerInfo['Fullname'],
      registerInfo['IdentityNumber'],
      registerInfo['Birthday'],
      registerInfo['Hometown'],
      registerInfo['Province'],
      registerInfo['District'],
      IdCardImage,
      SelfieImage
    )

    db.insertOCRForm(
      userId,
      ocrinfo['Fullname'],
      ocrinfo['IdentityNumber'],
      ocrinfo['Birthday'],
      ocrinfo['Hometown'],
      ocrinfo['Province'],
      ocrinfo['District']
    )

    db.insertResult(
      userId,
      face,
      0,
      verify['FullnameResult'],
      verify['IdentityNumberResult'],
      verify['BirthdayResult'],
      verify['HometownResult'],
      verify['ProvinceResult'],
      verify['DistrictResult'],
      verify['OCRResult']
    )
    
    return userId
  except Exception as e:
    print(e)
    return str(e)