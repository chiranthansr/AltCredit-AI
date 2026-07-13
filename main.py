from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import db
from routes.auth import router as auth_router
from routes.consent import router as consent_router
from routes.credit import router as credit_router
from routes.questionnaire import router as questionnaire_router
from routes.prediction import router as prediction_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(consent_router)

app.include_router(credit_router)

app.include_router(questionnaire_router)

app.include_router(prediction_router)
@app.get("/")
def home():
    return {
        "message": "Backend Working Successfully",
        "database": db.name
    }

