import boto3
from services.imageReader import toBase64Byte
from config.amazonConfig import AmazonConfig
from cryptography.fernet import Fernet

def compareFaces(sourceFile, targetFile):
  key_clock = Fernet(AmazonConfig['KEY_CLOCK'])
  access_clock = Fernet(AmazonConfig['ACCESS_CLOCK'])
  client = boto3.client(
    'rekognition',
    aws_access_key_id = key_clock.decrypt(AmazonConfig['ACCESS_KEY']),
    aws_secret_access_key = access_clock.decrypt(AmazonConfig['SECRET_KEY']),
    region_name = AmazonConfig['region_name']
  )
  sourceFile = toBase64Byte(sourceFile)
  targetFile = toBase64Byte(targetFile)
  response = client.compare_faces(SimilarityThreshold=80,
                                SourceImage={'Bytes': sourceFile},
                                TargetImage={'Bytes': targetFile})
  if len(response['FaceMatches']) == 0:
    return 0
  elif len(response['FaceMatches']) == 1:
    return response['FaceMatches'][0]['Similarity']