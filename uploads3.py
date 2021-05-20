import boto3

BUCKET='inboxgowhich'
OBJECT_NAME='computer_doctor_man.png'
'''
~/.aws/credentials（Windows ユーザーの場合は、C:\Users\USER_NAME\.aws\credentials）に
認証情報ファイルを作成し、下線部分の値を自分用の値に置き換えてから以下の行を保存します。

[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
'''
s3 = boto3.resource('s3')

bucket = s3.Bucket(BUCKET)
bucket.upload_file(OBJECT_NAME, OBJECT_NAME)

s3client = boto3.client('s3')

url = s3client.generate_presigned_url(
  ClientMethod = 'get_object',
  Params = {'Bucket' : BUCKET, 'Key' : OBJECT_NAME},
  ExpiresIn = 600,
  HttpMethod = 'GET')

print('-----\n{}\n-----'.format(url))
