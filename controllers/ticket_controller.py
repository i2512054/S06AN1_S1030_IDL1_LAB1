from fastapi import APIRouter, HTTPException, status
from models.ticket_dto import TicketRequestDTO, TicketClassificationDTO
from services.llm_service import LLMClassificationService

router = APIRouter(prefix="/api/v1/tickets", tags=["Ticket Classifier"])
llm_service = LLMClassificationService()

@router.post(
    "/classify", 
    response_model=TicketClassificationDTO, 
    status_code=status.HTTP_200_OK,
    summary="Clasificar un ticket de soporte empresarial mediante LLM"
)
async def classify_ticket_endpoint(request: TicketRequestDTO):
    if not request.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La descripción del ticket no puede estar vacía."
        )
    
    result = llm_service.classify_ticket(request)
    return result
