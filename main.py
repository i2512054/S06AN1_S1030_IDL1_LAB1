from fastapi import FastAPI
from controllers.ticket_controller import router as ticket_router

app = FastAPI(
    title="API de Clasificación de Tickets de Soporte SOA",
    description="Microservicio de triage de soporte técnico que utiliza IA para identificar arquitecturas de software empresarial.",
    version="1.0.0"
)

app.include_router(ticket_router)

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "Servicio de Clasificación de Tickets activo."}
