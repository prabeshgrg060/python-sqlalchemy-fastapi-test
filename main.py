from fastapi import FastAPI
from app.routers import user

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1', port=8000)

# Include routers here
app.include_router(user.router)