import uvicorn
from fastapi import FastAPI
from app.api import routes
from app.api import conversation
from app.api import stats

app = FastAPI(title="Multi_Agent_Software_Engineering_Assistant")

app.include_router(routes.router,prefix="/api/v1",tags=["LLM"])
app.include_router(conversation.router,prefix="/api/v1")
app.include_router(stats.router,prefix="/api/v1")



@app.get("/health")
def health_check():
    return {"message":"Ok from the server"}

def start():
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)

if __name__ == "__main__":
    start()
