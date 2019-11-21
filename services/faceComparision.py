import boto3
from services.imageReader import toBase64Byte
from config.amazonConfig import AmazonConfig
from services.crypto import decode

def compareFaces(sourceFile, targetFile):
  print("{}".format(decode(AmazonConfig['ACCESS_KEY']))[2:-1][:20])
  print("{}".format(decode(AmazonConfig['SECRET_KEY']))[2:-1][:40])
  # return 0
  client = boto3.client(
    'rekognition',
    aws_access_key_id = "{}".format(decode(AmazonConfig['ACCESS_KEY']))[2:-1][:20],
    aws_secret_access_key = "{}".format(decode(AmazonConfig['SECRET_KEY']))[2:-1][:40],
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