from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to send to the chat")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response")
    conversation_id: str = Field(..., description="Conversation ID")
    is_complete: bool = Field(default=False, description="Whether the conversation is complete")
    recommended_career: Optional[str] = Field(None, description="Recommended career if conversation is complete")
    recommended_faculty: Optional[str] = Field(None, description="Recommended faculty if conversation is complete")


class TranscriptionRequest(BaseModel):
    audio_format: str = Field(default="wav", description="Audio format")
    language: Optional[str] = Field("es", description="Language for transcription")


class TranscriptionResponse(BaseModel):
    transcription: str = Field(..., description="Transcribed text")
    confidence: Optional[float] = Field(None, description="Confidence score")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class ImageAnalysisRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for image analysis")


class ImageAnalysisResponse(BaseModel):
    analysis: str = Field(..., description="Analysis result from Gemini")
    filename: str = Field(..., description="Uploaded filename")


class HealthResponse(BaseModel):
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.now)


class CareerRecommendation(BaseModel):
    career: str = Field(..., description="Recommended career name")
    faculty: str = Field(..., description="Faculty name")
    confidence: float = Field(..., description="Confidence score of recommendation")
    reasoning: str = Field(..., description="Reasoning for the recommendation")


class ConversationSummary(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation identifier")
    total_messages: int = Field(..., description="Total number of messages in conversation")
    career_recommendation: Optional[CareerRecommendation] = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None)


class AudioUploadResponse(BaseModel):
    filename: str = Field(..., description="Uploaded audio filename")
    file_size: int = Field(..., description="File size in bytes")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    format: str = Field(..., description="Audio format")