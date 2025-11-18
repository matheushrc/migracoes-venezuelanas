from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "8501"))
    # Bind to 0.0.0.0 so the container accepts external connections
    uvicorn.run(app, host="0.0.0.0", port=port)
