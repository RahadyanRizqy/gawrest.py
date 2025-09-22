from fastapi import Request
from fastapi.responses import JSONResponse

async def root(request: Request):
    gemini_client = request.app.state.gemini_client
    return JSONResponse(
        content={"data": {
            "status": "ok",
            "gemini_client": gemini_client.running
        }}
    )