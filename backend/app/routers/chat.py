import base64
from fastapi import APIRouter, HTTPException
from typing import Dict, List
import uuid
import re
import google.generativeai as genai
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    ConversationSummary,
    CareerRecommendation
)
from app.config.settings import settings
import os
from dotenv import load_dotenv
from app.services.tts_service import TTSService

load_dotenv()

router = APIRouter(prefix="/chat", tags=["Chat"])

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

conversations: Dict[str, List[ChatMessage]] = {}
tts = TTSService()

def extract_career_recommendation(response_text: str) -> tuple[bool, str, str]:
    """
    Extrae la recomendación de carrera del texto de respuesta.
    Busca el patrón: "Tú perteneces a la Facultad [Nombre] y a la carrera [Nombre]."
    """
    pattern = r"Tú perteneces a la Facultad\s+([^y]+?)\s+y a la carrera\s+(.+?)\."
    match = re.search(pattern, response_text, re.IGNORECASE)

    if match:
        faculty = match.group(1).strip()
        career = match.group(2).strip()
        return True, faculty, career

    return False, "", ""

async def generate_gemini_response(conversation_history: List[ChatMessage], user_message: str) -> str:
    """
    Genera respuesta usando Gemini con el historial de conversación.
    """
    try:
        prompt_parts = [settings.prompt_system]

        for message in conversation_history:
            if message.role == "user":
                prompt_parts.append(f"Estudiante: {message.content}")
            else:
                prompt_parts.append(f"Sombrero Seleccionador: {message.content}")

        prompt_parts.append(f"Estudiante: {user_message}")
        prompt_parts.append("Sombrero Seleccionador:")

        full_prompt = "\n\n".join(prompt_parts)

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Envía un mensaje al chat y recibe respuesta del Sombrero Seleccionador.
    """
    try:
        if request.conversation_id == "":
            conversation_id = str(uuid.uuid4())
        else:
            conversation_id = request.conversation_id

        if conversation_id not in conversations:
            conversations[conversation_id] = []

        user_message = ChatMessage(role="user", content=request.message)
        conversations[conversation_id].append(user_message)

        ai_response = await generate_gemini_response(
            conversations[conversation_id],
            request.message
        )

        assistant_message = ChatMessage(role="assistant", content=ai_response)
        conversations[conversation_id].append(assistant_message)

        is_complete, faculty, career = extract_career_recommendation(ai_response)

        audio_file = tts.synthesize_and_save(ai_response)
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return ChatResponse(
            response=ai_response,
            audiob64=audio_base64,
            conversation_id=conversation_id,
            is_complete=is_complete,
            recommended_career=career if is_complete else None,
            recommended_faculty=faculty if is_complete else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@router.get("/conversation/{conversation_id}", response_model=List[ChatMessage])
async def get_conversation(conversation_id: str):
    """
    Obtiene el historial completo de una conversación.
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    return conversations[conversation_id]


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Elimina una conversación del historial.
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    del conversations[conversation_id]
    return {"message": "Conversación eliminada exitosamente"}

@router.get("/conversations", response_model=List[ConversationSummary])
async def list_conversations():
    """
    Lista todas las conversaciones activas.
    """
    summaries = []

    for conv_id, messages in conversations.items():
        is_complete = False
        career_rec = None

        if messages:
            last_message = messages[-1]
            if last_message.role == "assistant":
                is_complete, faculty, career = extract_career_recommendation(last_message.content)
                if is_complete:
                    career_rec = CareerRecommendation(
                        career=career,
                        faculty=faculty,
                        confidence=1.0,
                        reasoning="Determinado por el Sombrero Seleccionador"
                    )

        summary = ConversationSummary(
            conversation_id=conv_id,
            total_messages=len(messages),
            career_recommendation=career_rec,
            completed_at=messages[-1].timestamp if is_complete and messages else None
        )
        summaries.append(summary)

    return summaries
