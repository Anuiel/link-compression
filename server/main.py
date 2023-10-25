from uuid import uuid4, UUID
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI

redis_db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_db
    redis_db = redis.Redis(host='redis', port=6379, db=0)
    yield
    await redis_db.aclose()


app = FastAPI(lifespan=lifespan)


@app.post("/create")
async def cretae_shortcut(url : str):
    id = str(uuid4())
    await redis_db.set(id, url)
    return {"id": id}


@app.get("/link/{id}")
async def load_shortcut(id: UUID):
    cache = await redis_db.get(str(id))
    if cache is not None:
        return {'url': cache}
    else:
        return {"error": "eblan invalid"}