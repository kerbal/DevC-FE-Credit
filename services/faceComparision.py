import boto3
from services.imageReader import toBase64Byte
from config.amazonConfig import AmazonConfig

def compareFaces(sourceFile, targetFile):
  print(AmazonConfig)
  client = boto3.client(
    'rekognition',
    aws_access_key_id = AmazonConfig['ACCESS_KEY'],
    aws_secret_access_key = AmazonConfig['SECRET_KEY'],
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