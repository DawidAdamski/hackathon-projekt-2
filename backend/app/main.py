from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.routes.verification import router as verification_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()


# TODO: dodac jakis fake certyfikat do nginx i sciagac info z certyfikatu? ewentualnie z zamokowanej domenu gov
# TODO: Clenup na tokeny expire w token storage


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Start verifyer!")

    yield
    print("Stop verifyer!")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(verification_router, prefix="/verify")
