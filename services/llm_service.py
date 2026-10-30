import os
import json
from openai import OpenAI # geminiai
from google import genai
from google.genai import types
from dotenv import load_dotenv
from models.ticket_dto import TicketRequestDTO, TicketClassificationDTO, ArchitectureType, SeverityLevel

load_dotenv()

class LLMClassificationService:
    def __init__(self):
        # api_key = os.getenv("OPENAI_API_KEY")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")
        # self.client = OpenAI(api_key=api_key)
        self.client = genai.Client(api_key=api_key)

    def classify_ticket(self, request: TicketRequestDTO) -> TicketClassificationDTO:
        system_prompt = (
            "Eres un experto Ingeniero de Arquitectura de Software especializado en clasificar incidentes empresariales. "
            "Tu tarea es analizar la descripción de un ticket de soporte de retail e identificar:\n"
            "1. La arquitectura afectada: 'Monolithic' (sistemas legados todo-en-uno), 'Legacy ERP' (SAP, Oracle ERP, AS400), o 'SaaS Microservice' (servicios en la nube, APIs REST, checkout desacoplado).\n"
            "2. El nivel de severidad (LOW, MEDIUM, HIGH, CRITICAL).\n"
            "3. El equipo técnico especialista asignado.\n"
            "4. Una breve justificación de tu decisión."
        )
        user_prompt = (
            f"ID Ticket: {request.ticket_id}\nDescripción: {request.description}"
        )

        try:
            # Uso de Structured Outputs mediante parse de OpenAI SDK
            # completion = self.client.beta.chat.completions.parse(
            #     model="gpt-4o-mini",
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": f"ID Ticket: {request.ticket_id}\nDescripción: {request.description}"}
            #     ],
            #     response_format=TicketClassificationDTO,
            #     temperature=0.1
            # )
            completion = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=TicketClassificationDTO,
                    temperature=0.1
                ),
            )
            # return completion.choices[0].message.parsed
            return TicketClassificationDTO.model_validate_json(completion.text)

        except Exception as e:
            # Manejo de fallos en llamadas al LLM
            return TicketClassificationDTO(
                ticket_id=request.ticket_id,
                architecture_type=ArchitectureType.UNKNOWN,
                severity=SeverityLevel.HIGH,
                assigned_team="Triage Escalation Team",
                justification=f"Error durante el procesamiento del LLM: {str(e)}"
            )
