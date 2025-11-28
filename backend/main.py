from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core.workflow import run_repair_loop
from core.sandbox import execute_code

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    code: str

class RepairRequest(BaseModel):
    code: str

@app.post("/run")
async def run_code(req: RunRequest):
    result = execute_code(req.code)
    return result

@app.post("/repair")
async def repair_code(req: RepairRequest):
    history = run_repair_loop(req.code)
    return {"history": history}

@app.get("/health")
async def health():
    return {"status": "ok"}
