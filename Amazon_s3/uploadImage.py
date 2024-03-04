
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

#@app.route('/upload', methods=['POST'])
def upload_to_s3(image,side):
    try:
        s3.upload_fileobj(image, os.getenv('S3_BUCKET'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')+image.filename)
        linkName=side+ datetime.now().strftime('%Y-%m-%d %H:%M:%S')+image.filename


        return (True,linkName) # jsonify({'success': 'Image uploaded successfully'}), 200

    except Exception as e:
        return  (False,e)# jsonify({'error': str(e)}), 500
    
