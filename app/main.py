from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, users, arisans

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Yuk Arisan API",
    description="API untuk aplikasi arisan online",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(arisans.router, prefix="/api/v1/arisans", tags=["Arisans"])

@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Welcome to Yuk Arisan API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
