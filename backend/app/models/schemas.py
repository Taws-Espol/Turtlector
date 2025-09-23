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


class ImageAnalysisMetadata(BaseModel):
    image_path: str = Field(..., description="Path to the analyzed image")
    image_size: Optional[tuple] = Field(None, description="Image dimensions (width, height)")
    image_format: Optional[str] = Field(None, description="Image format (JPEG, PNG, etc.)")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    prompt_length: int = Field(..., description="Length of the prompt")
    model: str = Field(..., description="Model used for analysis")


class ImageAnalysisResponse(BaseModel):
    success: bool = Field(..., description="Whether the analysis was successful")
    analysis: Optional[str] = Field(None, description="Analysis result from Gemini")
    filename: str = Field(..., description="Uploaded filename")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    error_code: Optional[str] = Field(None, description="Error code for programmatic handling")
    metadata: Optional[ImageAnalysisMetadata] = Field(None, description="Analysis metadata")


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