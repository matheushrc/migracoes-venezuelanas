from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from routes import inference

app = FastAPI()
app.include_router(inference.router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "8501"))
    # Bind to 0.0.0.0 so the container accepts external connections
    uvicorn.run(app, host="0.0.0.0", port=port)
