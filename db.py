from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SAEnum
from datetime import datetime
import enum

SQLALCHEMY_DATABASE_URL = "sqlite:///./after_sales.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TicketStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    resolved = "resolved"
    closed = "closed"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default=TicketStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    """建表：只在程序启动时调用一次，必须传 engine，不能传 Session。"""
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
