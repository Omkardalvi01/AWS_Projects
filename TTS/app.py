from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import uvicorn
import boto3
import io
import re

s3 = boto3.client('s3')
audio_getter = boto3.client('lambda')

app = FastAPI()
def get_audio_for_pdf(pdf_filename):
    prefix = pdf_filename.replace('.pdf', '')
    response = s3.list_objects_v2(
        Bucket='tts-audio-file25', 
        Prefix=prefix
    )
    
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.mp3'):
            return obj['Key']
    return None

@app.post('/')
def post_text(file: UploadFile = File(...)):
    try:
        file_name = re.search('^\w+', file.filename).group()
        s3.upload_fileobj(file.file,'tts-text-file252',file_name)
        return {'response' : 'Uploaded'}
    except Exception as e:
        return {'response' : e}

@app.get('/get_audio/')
def get_audio(filename: str):
    try:
        audio_key = get_audio_for_pdf(filename)
        buffer = io.BytesIO()
        s3.download_fileobj(Bucket = 'tts-audio-file25', Key = audio_key , Fileobj = buffer)
        buffer.seek(0)
        return StreamingResponse(buffer, media_type='audio/mpeg')
    except Exception as e:
        print(e)
        return {'error' : e}

if __name__ =='__main__':
    uvicorn.run(app, port=8000)