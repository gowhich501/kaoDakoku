import boto3

# s3 = boto3.resource('s3')

KEY='AKIASD7LOLP7AS2DNWQT'
ACCESS_KEY='****'
BUCKET='inboxgowhich'
OBJECT_NAME='computer_doctor_man.png'


s3 = boto3.resource('s3',
        aws_access_key_id=KEY,
        aws_secret_access_key=ACCESS_KEY,
        region_name='ap-northeast-1'
)

bucket = s3.Bucket(BUCKET)
bucket.upload_file(OBJECT_NAME, OBJECT_NAME)

s3client = boto3.client('s3',
        aws_access_key_id=KEY,
        aws_secret_access_key=ACCESS_KEY,
        region_name='ap-northeast-1'
)

url = s3client.generate_presigned_url(
  ClientMethod = 'get_object',
  Params = {'Bucket' : BUCKET, 'Key' : OBJECT_NAME},
  ExpiresIn = 3600,
  HttpMethod = 'GET')

print('-----\n{}\n-----'.format(url))
