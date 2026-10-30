from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from db import get_db, Ticket, TicketStatus, SessionLocal
from .schemas import ChatRequest, ChatReply, TicketOut, TicketUpdate

router = APIRouter(tags=["售后"])


def _contains_after_sales(text: str) -> bool:
    """意图识别：命中售后关键词即判定为售后诉求。"""
    keywords = ["退款", "退货", "换货", "售后", "维修", "坏了", "破损", "漏发", "少发"]
    return any(k in text for k in keywords)


@router.post("/chat", response_model=ChatReply, summary="聊天：咨询或创建售后工单")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    message = req.message or ""

    if _contains_after_sales(message):
        ticket = Ticket(
            user_id=req.user_id,
            content=message,
            status=TicketStatus.pending,
            created_at=datetime.utcnow(),
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ChatReply(
            reply="已为您创建售后工单，客服将尽快处理",
            ticket_id=ticket.id,
        )

    return ChatReply(
        reply="您好，请问有什么可以帮您？（可输入“退款/退货/换货/售后”创建工单）",
        ticket_id=None,
    )


@router.get("/tickets", response_model=list[TicketOut], summary="查询某用户的全部工单")
def list_tickets(user_id: str, db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.user_id == user_id).order_by(Ticket.id.desc()).all()


@router.get("/tickets/{ticket_id}", response_model=TicketOut, summary="查询单个工单")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")
    return ticket


@router.patch("/tickets/{ticket_id}", response_model=TicketOut, summary="更新工单状态")
def update_ticket(ticket_id: int, body: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")
    if body.status is not None:
        ticket.status = body.status
    db.commit()
    db.refresh(ticket)
    return ticket
