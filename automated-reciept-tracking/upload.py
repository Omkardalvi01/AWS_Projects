from fastapi import FastAPI, UploadFile, File
import boto3
import uvicorn

app = FastAPI() 
s3 = boto3.client('s3')
@app.post('/')
def upload_pic(img : UploadFile = File(...)):
    try:
        s3.upload_fileobj(img.file ,'reciepts1212',img.filename)
        return {'result' : 'sucess'}
    except Exception as e:
        return {'error ' : e}

if __name__ == '__main__':
    uvicorn.run(app, port=8000)