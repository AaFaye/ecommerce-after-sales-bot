from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="用户唯一标识")
    message: str = Field(..., min_length=1, description="用户咨询内容")


class ChatReply(BaseModel):
    reply: str
    ticket_id: int | None


class TicketOut(BaseModel):
    id: int
    user_id: str
    content: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketUpdate(BaseModel):
    status: str | None = Field(None, description="工单新状态：pending/processing/resolved/closed")
