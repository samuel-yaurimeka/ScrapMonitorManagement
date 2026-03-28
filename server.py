from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="Ecommerce 2 API")

# --- Modelos de Datos ---
class ProcessItem(BaseModel):
    id: str
    display: str
    last_update: Optional[str] = None

class ProcessList(BaseModel):
    processes: List[ProcessItem] = []

# --- Base de datos en memoria (Temporal para el ejemplo) ---
# Nota: En Render, esto se vacía si el servidor se duerme o reinicia.
db = {
    "processes": []
}

@app.get("/")
def home():
    return {"status": "online", "message": "Ecommerce 2 API Running"}

# 1. Obtener todos los procesos
@app.get("/processes", response_model=List[ProcessItem])
def get_processes():
    return db["processes"]

# 2. Agregar o actualizar un proceso
@app.post("/processes")
def update_process(item: ProcessItem):
    # Generamos el timestamp en el servidor como pediste
    item.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Buscamos si ya existe el ID para actualizarlo, sino lo agregamos
    for idx, p in enumerate(db["processes"]):
        if p.id == item.id:
            db["processes"][idx] = item
            return {"message": "Proceso actualizado", "data": item}
    
    db["processes"].append(item)
    return {"message": "Proceso creado", "data": item}

# 3. Obtener un proceso específico por ID
@app.get("/processes/{process_id}")
def get_process(process_id: str):
    for p in db["processes"]:
        if p.id == process_id:
            return p
    raise HTTPException(status_code=404, detail="Proceso no encontrado")




