from fastapi import FastAPI

app = FastAPI(title="Purby API")


@app.get("/api/health")
async def health():
    return {"status": "ok"}