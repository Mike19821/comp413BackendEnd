
import boto3, botocore
import os
from dotenv import load_dotenv
import io
from datetime import datetime




load_dotenv()

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
   aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)


def upload_to_s3(image):
    try:
        linkName= datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+image.filename
        s=s3.upload_fileobj(image, os.getenv('S3_BUCKET'), linkName)
        
        print(s)
        



        return (True,linkName)

    except Exception as e:
        return  (False,e)# jsonify({'error': str(e)}), 500
    
def get_image_s3(image_name):
    response = s3.get_object(
    Bucket=os.getenv("S3_BUCKET"),
    Key=image_name)
    print("in s3", type(response))

    return response

