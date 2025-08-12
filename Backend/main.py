from fastapi import FastAPI,File,UploadFile,Request
import uvicorn

app=FastAPI()

@app.post('/upload')
async def endpoint(uploaded_file: UploadFile):
    content=await uploaded_file.read()
    print(content)
    return {"Hello":"Fastapi"}