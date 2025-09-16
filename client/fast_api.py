# server.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import uvicorn  # צריך להתקין עם pip install uvicorn

app = FastAPI()

UPLOAD_FOLDER = r"C:\pictures\uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return JSONResponse(content={"status": "ok", "id": file.filename})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

# ----------------------------
# הרצה ישירות מהקובץ
# ----------------------------
if __name__ == "__main__":
    uvicorn.run("ny_api:app", host="127.0.0.1", port=5000, reload=True)
