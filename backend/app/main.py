from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import todo_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_routes.router)

@app.get("/")
async def root():
    return {"message": "Todo API is running 🚀"}
