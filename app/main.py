import uvicorn
from fastapi import FastAPI
from app.api import routes
from app.utils.logging import logger

app = FastAPI(title="Multi_Agent_Software_Engineering_Assistant")
logger.info("Application started")
app.include_router(routes.router,prefix="/api/v1",tags=["LLM"])

@app.get("/health")
def health_check():
    return {"message":"Ok from the server"}

def start():
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)

if __name__ == "__main__":
    start()
