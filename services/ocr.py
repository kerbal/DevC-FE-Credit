from services.contour import findContour, fourPointTransform, orderPoints
import services.filter as filter
from services.imageReader import displayImage
import numpy as np 
from services.googleVision import OCR
import json

def parseId(id):
  res = ""
  for c in id:
    if c.isdigit():
      res += c
  return res

def parseBirthday(birthday):
  res = ""
  for c in birthday:
    if c.isdigit():
      res += c
      if len(res) == 2 or len(res) == 5:
        res += "-"
  return res

def extractInfo(text):
  text = text.lower()
  for c in ['|', '.', ':', '\n', '=', '…', '_']:
    text = text.strip().replace(c, ' ').strip()
  text = ' '.join(text.split())
  
  while text[-1].isalpha() == False:
    text = text[: -1]

  text = text.replace('đkhđ', 'đkhk')
  text = text.replace('đkhd', 'đkhk')
  text = text.replace('đkhh', 'đkhk')

  print(text)
  begin_number = text.find('số')
  begin_name = text.find('họ tên')
  begin_bd = text.find('sinh ngày')
  begin_address1 = text.find('nguyên quán')
  begin_address2 = text.find('trú')
  number = text[begin_number + 2 : begin_name].strip().replace(' ', '')
  name = text[begin_name + 6 : begin_bd].strip().replace('-', '').replace('  ', ' ')
  bd = text[begin_bd + 9: begin_address1].strip()
  hometown = text[begin_address1 + 11 : text.find("nơi")].strip().split(',')[-1].strip().replace('-', '').replace('  ', ' ')
  province = text[begin_address2 + 3 : ].strip().split(',')[-1].strip().replace('-', '').replace('  ', ' ')
  district = text[begin_address2 + 3 : ].strip().split(',')[-2].strip().replace('tp', '').strip().replace('-', '').replace('  ', ' ')

  return {
    'IdentityNumber': parseId(number),
    'Fullname': name.title(),
    'Birthday': parseBirthday(bd),
    'Hometown': hometown.title(),
    'Province': province.title(),
    'District': district.title()
  }

def ocr(image, registerInfo):
  image = filter.denoise(image)
  image = filter.grayScale(image)
  image = filter.denoiseGray(image)
  # image = filter.sharpen(image)
  # displayImage(image)

  info = extractInfo(OCR(image))

  print(info)
  verify = {
    'FullnameResult': info['Fullname'].lower() == registerInfo['Fullname'].lower(),
    'IdentityNumberResult': info['IdentityNumber'] == registerInfo['IdentityNumber'],
    'BirthdayResult': info['Birthday'] == registerInfo['Birthday'],
    'HometownResult': info['Hometown'].lower() == registerInfo['Hometown'].lower(),
    'ProvinceResult': info['Province'].lower() == registerInfo['Province'].lower(),
    'DistrictResult': info['District'].lower() == registerInfo['District'].lower()
  }

  verify['OCRResult'] = verify['FullnameResult'] and verify['IdentityNumberResult'] and verify['BirthdayResult'] and verify['HometownResult'] and verify['ProvinceResult'] and verify['DistrictResult']

  return info, verify