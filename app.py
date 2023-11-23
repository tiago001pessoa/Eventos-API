from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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

# Função para salvar os dados em um arquivo TXT
def save_to_txt(event: Event, event_id: int):
    # Limpar o conteúdo do arquivo antes de escrever os novos dados
    with open("dados.txt", "w") as file:
        pass
    
    # Adicionar os novos dados ao arquivo
    with open("dados.txt", "a") as file:
        file.write(f"Evento ID: {event_id}\n")
        file.write(f"Title: {event.title}\n")
        file.write(f"Description: {event.description}\n")
        file.write(f"Date: {event.date}\n")
        file.write(f"Time: {event.time}\n")
        file.write(f"Location: {event.location}\n")
        file.write(f"Cost: {event.cost}\n")
        file.write("\n")

# Criando CRUD para Evento

# Rota para criar um evento
@app.post("/eventos/", response_model=Event)
def create_event(event: Event):
    """
    Cria um novo evento.

    Args:
        - event: Informações sobre o evento a ser criado.

    Returns:
        Dados do evento recém-criado.
    """
    event_id = len(database) + 1
    database[event_id] = event
    save_to_txt(event, event_id)
    return JSONResponse(content={"message": "Evento criado com sucesso", "event_id": event_id, "event": event.dict()})

# Rota para listar todos os eventos
@app.get("/eventos/")
def list_events():
    """
    Obtém detalhes de um evento por ID.

    Args:
        - evento_id: ID do evento a ser obtido.

    Returns:
        Dados do evento com o ID especificado.
    """
    return database

# Rota para atualizar um evento por ID
@app.put("/eventos/{evento_id}")
def update_event(evento_id: int, event: Event):
    """
    Atualiza um evento existente por ID.

    Args:
        - evento_id: ID do evento a ser atualizado.
        - event: Novas informações do evento.

    Returns:
        Mensagem de sucesso após a atualização.

    Raises:
        HTTPException (404): Se o evento não for encontrado.
    """
    if evento_id not in database:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    database[evento_id] = event
    save_to_txt(event, evento_id)
    return {"message": f"Evento com ID {evento_id} atualizado com sucesso"}

# Rota para deletar um evento por ID
@app.delete("/eventos/{evento_id}")
def delete_event(evento_id: int):
    """
    Deleta um evento por ID.

    Args:
        - evento_id: ID do evento a ser deletado.

    Returns:
        Mensagem de sucesso após a exclusão.

    Raises:
        HTTPException (404): Se o evento não for encontrado.
    """
    if evento_id not in database:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    # Salvar os dados antes de excluir o evento
    event = database[evento_id]
    save_to_txt(event, evento_id)
    
    # deletando da memoria
    del database[evento_id]
    return {"message": f"Evento com ID {evento_id} deletado com sucesso"}
