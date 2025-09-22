import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from web.routes import router
from gemini_webapi import GeminiClient
from gemini_webapi import logger
from utils.extract_cookies import extract_cookies
from utils.replace_logger import *

from dotenv import dotenv_values

# Load environment variables
_config = dotenv_values(".env")

config = {
    "port": int(_config.get("PORT", 5800)),              # default 5800
    "cookie_header": _config.get("COOKIE_HEADER", ""),   # default kosong
    "secret_key": _config.get("SECRET_KEY", "changeme"), # default 'changeme'
    "log_level": _config.get("LOG_LEVEL", "INFO"),       # default 'INFO'
}

# Load cookies from file
cookies_txt_path = "./cookies.txt"
if (config["cookie_header"] == ""):
    try:
        with open(cookies_txt_path, "r", encoding="utf-8") as f:
            config["cookie_header"] = f.read().strip()  # baca seluruh isi file
    except FileNotFoundError:
        config["cookie_header"] = ""
        print(f"Warning: {cookies_txt_path} not found. Cookie header empty.")

# Load cookies
cookies = extract_cookies(config["cookie_header"])

# Initialize Gemini client
gemini_client = GeminiClient(cookies["__Secure-1PSID"], cookies["__Secure-1PSIDTS"], proxy=None)

# FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await gemini_client.init(timeout=300, auto_close=False, close_delay=300, auto_refresh=True)
    logger.info("Gemini client initialized")
    yield
    logger.warning("Gemini client closed")

# FastAPI app
app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.state.config = config
app.state.gemini_client = gemini_client

# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config["port"],
        log_config=None
    )
