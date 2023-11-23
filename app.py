from fastapi import FastAPI, HTTPException, Form, Query
from typing import Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="API de Gerenciamento de Eventos",
    description="Uma API para criar, listar, atualizar e excluir eventos.",
)

# Modelando o elemento Evento usando Pydantic
class Event(BaseModel):
    title: str
    description: str
    date: str
    time: str
    location: str
    cost: str

database: Dict[int, Event] = {}
next_event_id = 1  # Inicializamos com 1 para evitar problemas com IDs repetidos

# Função para salvar os dados em um arquivo TXT
def save_to_txt():
    with open("dados.txt", "w") as file:
        for event_id, event in database.items():
            file.write(f"Evento ID: {event_id}\n")
            file.write(f"Title: {event.title}\n")
            file.write(f"Description: {event.description}\n")
            file.write(f"Date: {event.date}\n")
            file.write(f"Time: {event.time}\n")
            file.write(f"Location: {event.location}\n")
            file.write(f"Cost: {event.cost}\n")
            file.write("\n")

# Criando CRUD para Evento

# Renderizando home
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/eventos/formulario", response_class=HTMLResponse)
def exibir_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Rota para criar um evento
@app.post("/eventos/", response_model=Event)
def create_event(event: Event):
    global next_event_id
    event_id = next_event_id
    next_event_id += 1
    database[event_id] = event
    save_to_txt()
    return JSONResponse(content={"message": "Evento criado com sucesso", "event_id": event_id, "event": event.dict()})

# Rota para adicionar um evento usando formulário HTML
@app.post("/eventos/adicionar", response_class=HTMLResponse)
def adicionar_evento(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    location: str = Form(...),
    cost: str = Form(...),
):
    global next_event_id
    event_id = next_event_id
    next_event_id += 1
    new_event = Event(
        title=title,
        description=description,
        date=date,
        time=time,
        location=location,
        cost=cost
    )
    database[event_id] = new_event
    save_to_txt()
    return HTMLResponse(content=f"<html><body><p>Evento adicionado com sucesso!</p></body></html>")

# Rota para listar todos os eventos
@app.get("/eventos/", response_model=Dict[int, Event])
def list_events():
    return database

# Exemplo de consulta usando um parâmetro 'title'
@app.get("/eventos/consulta")
def consulta_evento(title: str = Query(..., description="Título do evento para consulta")):
    for evento_id, event in database.items():
        if event.title == title:
            return {evento_id: event.dict()}

    raise HTTPException(status_code=404, detail=f"Evento com título '{title}' não encontrado.")

# Rota para atualizar um evento por ID
@app.put("/eventos/{event_id}")
def update_event(event_id: int, event: Event):
    if event_id not in database:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    database[event_id] = event
    save_to_txt()
    return {"message": f"Evento com ID {event_id} atualizado com sucesso"}

# Rota para deletar um evento por ID
@app.delete("/eventos/{event_id}")
def delete_event(event_id: int):
    if event_id not in database:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    del database[event_id]
    save_to_txt()
    return {"message": f"Evento com ID {event_id} deletado com sucesso"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
