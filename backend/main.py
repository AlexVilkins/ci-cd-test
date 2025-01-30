import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from grpc_utils.proto_ws.server import serve
from youtube.youtube_router import router as youtube_router
import betterlogging as bl


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(serve())
    yield


setup_logging()

app = FastAPI(title="YouTube App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_router)


uvicorn.run(app, host="0.0.0.0", port=8000)
#uvicorn.run(app, host="localhost", port=8030)
