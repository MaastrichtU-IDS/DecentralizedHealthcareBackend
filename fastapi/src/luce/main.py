from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, select
from sqlalchemy import func

from luce.config import settings, init_db, engine
from luce.users import CreateUser, User, router as users_router
from brownie import network, project


p = project.load("brownie", name="BrownieProject")
p.load_config()
# network.connect("development")
network.connect("luce")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    init_db()
    # Register admin user if no users are present
    with Session(engine) as session:
        user_count = session.scalar(select(func.count(User.email)))
        if user_count == 0:
            print(f"⚠️ No user found, initializing {settings.admin_email} user.")
            admin_user = CreateUser(
                email=settings.admin_email,
                password=settings.admin_password,
                first_name="user",
                last_name="admin",
                institution="Maastricht University",
                user_type=0,
                gender=0,
                age="25",
                country="Netherlands",
                ethereum_public_key="0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
                ethereum_private_key="0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3",
            )
            session.add(User.from_orm(admin_user))
            session.commit()
    yield


app = FastAPI(
    title="LUCE blockchain API",
    description="""API for the LUCE blockchain.

If you are facing issues, contact [vincent.emonet@maastrichtuniversity.nl](mailto:vincent.emonet@maastrichtuniversity.nl)""",
    lifespan=lifespan,
)

app.include_router(users_router)
# app.include_router(auth_router)

# TODO: "/contract/dataUpload/" in healthcare/views.py

# @app.post(
#     "/upload",
#     response_description="Upload result",
#     response_model={},
# )
# async def upload_files(
#     user: Any = Depends(get_user_info),
#     cohort_id: str = Form(..., pattern="^[a-zA-Z0-9-_]+$"),
#     cohort_dictionary: UploadFile = File(...),
#     cohort_data: UploadFile | None = None,
# ) -> dict[str, str]:
#     """Upload files to the server"""
#     # Create directory named after cohort_id
#     cohorts_folder = os.path.join(settings.data_folder, "cohorts", cohort_id)
#     os.makedirs(cohorts_folder, exist_ok=True)
    # print("USER", user)


@app.get("/", include_in_schema=False)
def redirect_root_to_docs() -> RedirectResponse:
    """Redirect the route / to /docs"""
    return RedirectResponse(url="/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
