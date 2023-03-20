from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

connection = sqlite3.connect('operation_registers.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS registers 
                (id INTEGER PRIMARY KEY, operation_type TEXT, status TEXT, ope_start_time TEXT, ope_end_time TEXT)''')
connection.commit()

class Register(BaseModel):
    operation_type: str
    status: str = None
    ope_start_time: str = None
    id: int = 0

@app.get("/")
def root():
    return {"Test" : "Fast API"}

@app.post("/register")
def create_operation(data: Register):
    ope_end_time = datetime.utcnow().timestamp()

    cursor.execute("INSERT INTO registers (operation_type, status, ope_start_time, ope_end_time) VALUES (?, ?, ?, ?)", 
                (data.operation_type, data.status, data.ope_start_time, ope_end_time))
    connection.commit()
    return {
            "id": data.id, 
            "operation_type": data.operation_type,
            "status": data.status,
            "ope_start_time": data.ope_start_time,
            "ope_end_time": ope_end_time
        }

@app.get("/register")
def get_operations(status: str = None):
    if status is None:
        cursor.execute("SELECT * FROM registers")
    else:
        cursor.execute("SELECT * FROM registers WHERE status = ?", (status,))
    rows = cursor.fetchall()
    return [{"id": row[0], "operation_type": row[1], "status": row[2], "ope_start_time": row[3], "ope_end_time": row[4]} for row in rows]


@app.put("/register/{item_id}")
def update_operation(item_id: int, data: Register):
    ope_end_time = datetime.utcnow().timestamp()
    cursor.execute("UPDATE registers SET operation_type = ?, status = ?,  ope_start_time = ?, ope_end_time = ? WHERE id = ?", 
                (data.operation_type, data.status, data.ope_start_time, ope_end_time, item_id))
    connection.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Invalid id.")
    return {
            "id": item_id,
            "operation_type": data.operation_type, 
            "status": data.status, 
            "ope_end_time": ope_end_time
        }

@app.delete("/register/{op_id}")
def delete_operation(op_id: int):
    cursor.execute("DELETE FROM registers WHERE id = ?", (op_id,))
    connection.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Invalid id.")
    return {"message": "Frame register deleted"}
