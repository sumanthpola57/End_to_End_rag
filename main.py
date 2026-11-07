import logging
import os

import psycopg
from fastapi import FastAPI, HTTPException

# 1. Logbook setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# 2. Settings from outside the code
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rag:rag@localhost:5432/rag",
)

# 3. The waiter
app = FastAPI()


@app.get("/health_check")
def health_check():
    return {"status": "healthy"}


@app.get("/db_check")
def db_check():
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        logger.info("Database check passed")
        return {"db": "ok"}
    except psycopg.OperationalError:
        logger.exception("Database check failed")
        raise HTTPException(status_code=503, detail="database unavailable")