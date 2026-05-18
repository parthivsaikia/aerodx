from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/analyze")
async def analyze_scan(file: UploadFile):
    return {
        "prediction": "Pneumonia",
        "confidence": 0.91,
        "summary": "Possible pneumonia detected"
    }
