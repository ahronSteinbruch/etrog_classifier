# filename: api_server.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    size = len(content)
    return JSONResponse(content={"filename": file.filename, "size": size, "status": "received"})
if __name__ == "__main__":
    # מפעיל את השרת כשהקובץ רץ ישירות
    uvicorn.run("fast_api:app", host="127.0.0.1", port=8000, reload=True)