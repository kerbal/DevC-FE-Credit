from services.imageReader import readURL, readb64, displayImage, toBase64
from services.ocr import ocr
from services.faceComparision import compareFaces
import services.database as db
from services.temp import compare_quochuy, compare_tieude
from services.contour import cropContour

def main(IdCardImage, SelfieImage, registerInfo):
  try:
    idCardImage = readb64(IdCardImage)
    selfieImage = readb64(SelfieImage)
    croppedIdCard, success = cropContour(idCardImage)
  
    # face comparision
    face = 0
    croppedFace = ""
    if success == True:
      croppedFace = croppedIdCard[
        int(0.425 * croppedIdCard.shape[0]) : int(0.9 * croppedIdCard.shape[0]),
        int(0.04 * croppedIdCard.shape[1]) : int(0.275 * croppedIdCard.shape[1])
      ]
      face = compareFaces(croppedFace, selfieImage)
    else:
      croppedFace = idCardImage
      face = compareFaces(idCardImage, selfieImage)

    # OCR
    ocrinfo = {} 
    verify = {}
    if success == True:
      croppedOCR = croppedIdCard[
        int(croppedIdCard.shape[0] * 0.225) : croppedIdCard.shape[0], 
        int(croppedIdCard.shape[1] * 0.3) : croppedIdCard.shape[1]
      ]
      ocrinfo, verify = ocr(croppedOCR, registerInfo)
    else:
      ocrinfo, verify = ocr(idCardImage, registerInfo)

    quocHuyScore = 0
    quocNguScore = 0
    tenGiayScore = 0
    tieuNguScore = 0
    if success == True:
      quocHuyScore, quocHuyCropped = compare_quochuy(croppedIdCard)
      quocNguScore, tenGiayScore, tieuNguScore, tieuDeCropped = compare_tieude(croppedIdCard)
    else:
      quocHuyScore, quocHuyCropped = compare_quochuy(idCardImage)
      quocNguScore, tenGiayScore, tieuNguScore, tieuDeCropped = compare_tieude(idCardImage)

    print('Face:', face)
    print('OCR:', ocrinfo)
    print('Quoc huy:', quocHuyScore)
    print('Quoc ngu:', quocNguScore)
    print('Ten giay:', tenGiayScore)
    print('Tieu ngu:', tieuNguScore)
    # displayImage(croppedFace)
    # displayImage(croppedIdCard)
    # displayImage(quocHuyCropped)
    # displayImage(tieuDeCropped)
    # return

    # return 
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

    # return
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
      verify['FullnameResult'],
      verify['IdentityNumberResult'],
      verify['BirthdayResult'],
      verify['HometownResult'],
      verify['ProvinceResult'],
      verify['DistrictResult'],
      verify['OCRResult'],
      quocHuyScore,
      quocNguScore,
      tenGiayScore,
      tieuNguScore,
    )
    
    print('inserted result')
    db.insertImages(
      userId, 
      toBase64(croppedIdCard).decode("utf-8"), 
      toBase64(quocHuyCropped).decode("utf-8"), 
      toBase64(tieuDeCropped).decode("utf-8"), 
      toBase64(croppedFace).decode("utf-8")
    )

    return {
      'success': True,
      'userId': userId
    }
  except Exception as e:
    print(e)
    return {
      'success': False,
      'message': str(e)
    }