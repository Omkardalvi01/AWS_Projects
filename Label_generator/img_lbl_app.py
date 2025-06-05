import boto3 
from fastapi import FastAPI, UploadFile, File
import re 
import uvicorn
app = FastAPI()

rec = boto3.client('rekognition')
s3 = boto3.client('s3')
@app.post('/')
def predit(file: UploadFile = File(...)):
    file_name = re.search('^\w+', file.filename)
    s3.upload_fileobj(file.file , 'img-label', file_name.group())
    responses = rec.detect_labels(Image={'S3Object': {'Bucket' : 'img-label', 'Name' : file_name.group()}}, MaxLabels = 3)
    result = dict()
    for i in range(3):
        result[responses['Labels'][:][:][i]['Name']] = responses['Labels'][:][:][i]['Confidence']

    return {'result' : result}

if __name__ == "__main__":
    uvicorn.run(app, port= 8000)
