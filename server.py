from fastapi import FastAPI

app = FastAPI(title="Multi_Agent_Software_Engineering_Assistant")


@app.get("/health")
def health_check():
    return {"message":"Ok from the server"}