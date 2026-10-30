from pydantic import BaseModel, Field
from enum import Enum

class ArchitectureType(str, Enum):
    MONOLITHIC = "Monolithic"
    LEGACY_ERP = "Legacy ERP"
    SAAS_MICROSERVICE = "SaaS Microservice"
    UNKNOWN = "Unknown"

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TicketRequestDTO(BaseModel):
    ticket_id: str = Field(..., example="TCK-9821")
    description: str = Field(..., example="El sistema de facturación SAP emite un error de conexón a la base de datos Hana durante el cierre de caja.")

class TicketClassificationDTO(BaseModel):
    ticket_id: str = Field(..., description="Identificador único del ticket")
    architecture_type: ArchitectureType = Field(..., description="Tipo de arquitectura de aplicación afectada")
    severity: SeverityLevel = Field(..., description="Nivel de severidad asignado al problema")
    assigned_team: str = Field(..., description="Equipo técnico asignado para resolver la incidencia")
    justification: str = Field(..., description="Explicación técnica simplificada del motivo de la clasificación")