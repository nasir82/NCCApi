from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import administration_router, event_router, exam_rounter, office_router, payment_router, resource_router, teachers_router
from .models import models
from .router import banner_router, student_router, user_router, attendance_router
from .database.database import engine


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="NCC Management System API",
    description="""...""",
    version="1.0.1",
    lifespan=lifespan,
    contact={
        "name": "NCC Support",
        "email": "nasirpks36@gmail.com",
    },
)
# app = FastAPI(
#     title="NCC Management System API",
#     description="""
# This API handles all internal operations for NCC, including:
# * **Attendance Tracking** for students.
# * **Payment Management** for fees and records.
# * **Exam & Resource** distribution.
#     """,
#     version="1.0.1",
#     contact={
#         "name": "NCC Support",
#         "email": "nasirpks36@gmail.com",
#     },
# )
# models.Base.metadata.create_all (bind= engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers = ["*"]
)

app.include_router(banner_router.router)
app.include_router(student_router.router)
app.include_router(user_router.router)
app.include_router(administration_router.router)
app.include_router(attendance_router.router)
app.include_router(event_router.router)
app.include_router(exam_rounter.router)
app.include_router(payment_router.router)
app.include_router(resource_router.router)
app.include_router(office_router.router)
app.include_router(teachers_router.router)

@app.get("/")
def home():
    return {"Welcome": "To the FastAPI application!", "status": "running"}



"""
Next todo:
slowapi -> prevent DDoS attack
"""




"""
for binding port like nodejs express

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

"""To run the FastAPI application, use the following command in your terminal:
    uvicorn main:app --host 0.0.0.0 --port 8000
    with auto reload on code changes, add the --reload flag:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

"""

"""
pip install passlib
pip install "passlib[bcrypt]"
.\venv\Scripts\Activate.ps1
netstat -ano | findstr :8000
taskkill 3852 from powershell with administration
taskkill /F /PID 3852
pip install "python-jose[cryptography]"
"""


"""
pip install alembic
alembic init alembic
"""