from fastapi import FastAPI, HTTPException
from datetime import datetime
from database import Database
from pydantic import BaseModel

app = FastAPI()

class Register(BaseModel):
    operation_type: str
    status: str = None
    ope_start_time: str = None
    id: int = 1

db = Database()

@app.post("/register")
def create_operation(data: Register):
    ope_end_time = datetime.utcnow().timestamp()
    register_id = db.insert_register(data.operation_type, data.status, data.ope_start_time, ope_end_time)
    return {
            "id": register_id, 
            "operation_type": data.operation_type,
            "status": data.status,
            "ope_start_time": data.ope_start_time,
            "ope_end_time": ope_end_time
        }

@app.get("/register")
def get_operations(status: str = None):
    return db.get_registers(status)

@app.put("/register/{register_id}")
def update_operation(register_id: int, data: Register):
    ope_end_time = datetime.utcnow().timestamp()
    rows_affected = db.update_register(register_id, data.operation_type, data.status, data.ope_start_time, ope_end_time)
    if rows_affected < 1:
        raise HTTPException(status_code=404, detail="Invalid id.")
    return {
            "id": register_id,
            "operation_type": data.operation_type, 
            "status": data.status,
            "ope_start_time": data.ope_start_time,
            "ope_end_time": ope_end_time
    }