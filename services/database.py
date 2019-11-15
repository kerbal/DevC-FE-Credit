import sqlalchemy
from sqlalchemy import create_engine
from datetime import datetime
from math import floor
import sys

dburi = ''
if len(sys.argv) == 3:
  dburi = 'postgres://whghbahrsilwgi:e42dc554baed5f277851a6beda9984036ac56ad7a0527a4cb4c1f7f6d208b67b@ec2-107-21-94-185.compute-1.amazonaws.com:5432/d9ga0aonco08mb'
else:
  dburi = 'postgresql://khanh:1234@localhost:5432/devcfe'
engine = create_engine(dburi)

def getCurrentTimestamp():
  return floor(datetime.timestamp(datetime.now())) * 1000

def executeQuery(sql):
  response = None
  with engine.connect() as con:
    rs = con.execute(sql)
    response = rs
    con.close()
  return response

def insertUser(PhoneNumber):
  now = getCurrentTimestamp()
  executeQuery("""insert into "User" ("PhoneNumber", "VerificationStatus", "CreatedAt") values ('{}', {}, '{}')""".format(PhoneNumber, False, now))
  response = executeQuery("""select * from "User" where "PhoneNumber" =  '{}' and "CreatedAt" = '{}' """.format(PhoneNumber, now))
  for row in response:
    return row[0]

def getUserById(id):
  response = executeQuery("""select * from "User" where "Id" = {} """.format(id))
  for row in response:
    return row

def insertRegisterForm(userId, fullname, identityNumber, birthday, hometown, province, district, identityCardImage, selfieImage):
  now = getCurrentTimestamp()
  executeQuery("""insert into "RegisterForm" ("UserId", "Fullname", "IdentityNumber", "Birthday", "Hometown", "Province", "District", "IdentityCardImage", "SelfieImage") values ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(userId, fullname, identityNumber, birthday, hometown, province, district, identityCardImage, selfieImage))

def insertOCRForm(userId, fullname, identityNumber, birthday, hometown, province, district):
  now = getCurrentTimestamp()
  executeQuery("""insert into "OCRInformation" ("UserId", "Fullname", "IdentityNumber", "Birthday", "Hometown", "Province", "District") values ({}, '{}', '{}', '{}', '{}', '{}', '{}')""".format(userId, fullname, identityNumber, birthday, hometown, province, district))

def insertResult(userId, faceResult, templateResult, fullnameResult, identityNumberResult, birthdayResult, hometownResult, provinceResult, districtResult, ocrResult):
  now = getCurrentTimestamp()
  executeQuery("""insert into "Result" ("UserId", "FaceResult", "TemplateResult", "FullnameResult", "IdentityNumberResult", "BirthdayResult", "HometownResult", "ProvinceResult", "DistrictResult", "OCRResult") values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(userId, faceResult, templateResult, fullnameResult, identityNumberResult, birthdayResult, hometownResult, provinceResult, districtResult, ocrResult))

def getUserResult():
  response = executeQuery("""select "User"."Id", "User"."PhoneNumber", "User"."VerificationStatus", "Result"."OCRResult", "Result"."FaceResult", "Result"."TemplateResult" from "User" join "Result" on "User"."Id" = "Result"."UserId" """)
  result = []
  for row in response:
    result.append({
      "UserId": row[0],
      "PhoneNumber": row[1],
      "VerificationStatus": row[2],
      "OCRResult": row[3],
      "FaceResult": row[4],
      "TemplateResult": row[5]
    })
  return result

def getUserResultById(id):
  response = executeQuery(""" select * from "User", "RegisterForm", "OCRInformation", "Result" where "User"."Id" = "RegisterForm"."UserId" and "User"."Id" = "OCRInformation"."UserId" and "User"."Id" = "Result"."UserId" and "User"."Id" = {} """.format(id))
  result = {}
  for row in response:
    i = 0
    for key in row.keys():
      result[key] = row[i]
      i += 1
  return result

def getVerificationStatus(id):
  response = executeQuery(""" select "User"."VerificationStatus" from "User" where "User"."Id" = {} """.format(id))
  for row in response:
    return row[0]

def setVerificationStatus(id, status):
  print(id, status)
  executeQuery(""" update "User" set "VerificationStatus" = {} where "User"."Id" = {} """.format(status, id))