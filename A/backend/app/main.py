from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, auth

#uvicorn app.main:app --reload  ##fetch('http://localhost:8000/').then(res => res.json()).then(console.log)

app = FastAPI()

origins = ["*"]

app.add_middleware( 
    CORSMiddleware, #middleware runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"hello there"}
